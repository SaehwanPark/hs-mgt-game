import subprocess
import json
import sys
import os
import select
import shlex
import time

class McpClient:
  def __init__(self, bin_path=None, timeout_seconds=10):
    if bin_path is None:
      bin_path = os.environ.get("HS_MGT_GAME_MCP_BIN")
      if bin_path is None:
        local_bin = "./target/debug/hs-mgt-game-mcp"
        bin_path = local_bin if os.path.exists(local_bin) else "cargo run --quiet --bin hs-mgt-game-mcp"
    self.bin_path = bin_path
    self.proc = None
    self.msg_id = 0
    self.timeout_seconds = timeout_seconds
    self.last_method = None
    self.read_buffer = b""

  def start(self):
    cmd = shlex.split(self.bin_path)
    self.proc = subprocess.Popen(
      cmd,
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      bufsize=0
    )
    self._initialize()

  def _send(self, method, params=None, is_notification=False):
    self.msg_id += 1
    self.last_method = method
    msg = {
      "jsonrpc": "2.0",
      "method": method
    }
    if params is not None:
      msg["params"] = params
    if not is_notification:
      msg["id"] = self.msg_id

    payload = json.dumps(msg)
    self.proc.stdin.write((payload + "\n").encode("utf-8"))
    self.proc.stdin.flush()
    return self.msg_id

  def _recv(self, expected_id=None):
    deadline = time.monotonic() + self.timeout_seconds
    while True:
      if b"\n" not in self.read_buffer:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
          raise TimeoutError(self._timeout_message(expected_id))
        ready, _, _ = select.select([self.proc.stdout.fileno()], [], [], remaining)
        if not ready:
          raise TimeoutError(self._timeout_message(expected_id))
        chunk = os.read(self.proc.stdout.fileno(), 4096)
        if not chunk:
          raise EOFError(
            "MCP server process closed connection unexpectedly."
            + self._stderr_excerpt()
          )
        self.read_buffer += chunk
        if b"\n" not in self.read_buffer:
          continue
      remaining = deadline - time.monotonic()
      if remaining <= 0:
        raise TimeoutError(self._timeout_message(expected_id))
      line, self.read_buffer = self.read_buffer.split(b"\n", 1)
      try:
        msg = json.loads(line.decode("utf-8"))
      except json.JSONDecodeError:
        continue

      if "id" in msg:
        if expected_id is not None and msg["id"] != expected_id:
          continue
        return msg

  def _initialize(self):
    req_id = self._send("initialize", {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "playtest-client", "version": "1.0"}
    })
    res = self._recv(req_id)
    if "error" in res:
      raise RuntimeError(f"Initialization failed: {res['error']}")
    self._send("notifications/initialized", is_notification=True)

  def call_tool(self, tool_name, arguments):
    req_id = self._send("tools/call", {
      "name": tool_name,
      "arguments": arguments
    })
    res = self._recv(req_id)
    if "error" in res:
      return {"isError": True, "error": res["error"]}
    
    result = res.get("result", {})
    if result.get("isError"):
      error_content = result.get("content", [{}])[0].get("text", "Unknown tool error")
      return {"isError": True, "error": error_content}
      
    if "structuredContent" in result:
      return {"isError": False, "data": result["structuredContent"]}
    else:
      try:
        text_content = result["content"][0]["text"]
        return {"isError": False, "data": json.loads(text_content)}
      except Exception:
        return {"isError": False, "data": result}

  def close(self):
    if self.proc:
      if self.proc.stdin:
        self.proc.stdin.close()
      try:
        self.proc.wait(timeout=5)
      except subprocess.TimeoutExpired:
        self.proc.kill()

  def _timeout_message(self, expected_id):
    detail = (
      f"Timed out after {self.timeout_seconds}s waiting for MCP response"
      f" to request id {expected_id} ({self.last_method})."
    )
    return detail + self._stderr_excerpt()

  def _stderr_excerpt(self):
    if not self.proc or not self.proc.stderr:
      return ""
    ready, _, _ = select.select([self.proc.stderr.fileno()], [], [], 0)
    if not ready:
      return ""
    try:
      text = os.read(self.proc.stderr.fileno(), 4000).decode("utf-8", errors="replace")
    except BlockingIOError:
      return ""
    if not text:
      return ""
    return f"\nMCP server stderr excerpt:\n{text}"

def play_session(campaign, seed=42, difficulty="normal", policy_fn=None):
  client = McpClient()
  client.start()
  
  try:
    args = {"campaign": campaign, "seed": seed}
    if campaign == "competitive-regional-v1":
      args["difficulty"] = difficulty
        
    res = client.call_tool("start_session", args)
    if res["isError"]:
      print(f"Error starting session: {res['error']}")
      return None
        
    session = res["data"]
    session_id = session["session_id"]
    history = []
    validation_failures = []
    
    while not session["done"]:
      turn = session["turn"]
      obs = session["observation"]
      legal = session["legal_commands"]
      
      if policy_fn:
        cmd = policy_fn(obs, legal, turn)
      else:
        print(f"\n--- Turn/Month {turn} ---")
        print("\n".join(obs))
        print(f"Legal command description/hints: {legal}")
        cmd = input("Enter command: ")
          
      res = client.call_tool("submit_turn", {
        "session_id": session_id,
        "command_text": cmd
      })
      
      if res["isError"]:
        failure = {
          "turn": turn,
          "command": cmd,
          "error": res["error"]
        }
        validation_failures.append(failure)
        if policy_fn:
          raise RuntimeError(
            f"Scripted policy failed on {campaign} turn {turn} with command "
            f"{cmd!r}: {res['error']}"
          )
        if not policy_fn:
          print(f"\n[Validation Error] {res['error']}")
          print("Please try again.")
        continue
          
      session = res["data"]
      if session.get("latest_transition"):
        history.append(session["latest_transition"])
            
    res = client.call_tool("end_session", {"session_id": session_id})
    debrief = res["data"].get("debrief", []) if not res["isError"] else ["Failed to end session."]
    
    return {
      "campaign": campaign,
      "seed": seed,
      "difficulty": difficulty if campaign == "competitive-regional-v1" else None,
      "history": history,
      "debrief": debrief,
      "final_observation": session["observation"],
      "validation_failures": validation_failures
    }
  finally:
    client.close()

if __name__ == "__main__":
  campaign = sys.argv[1] if len(sys.argv) > 1 else "stabilization-v1"
  play_session(campaign)
