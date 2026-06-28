import subprocess
import json
import sys
import os

class McpClient:
  def __init__(self, bin_path="cargo run --bin hs-mgt-game-mcp"):
    self.bin_path = bin_path
    self.proc = None
    self.msg_id = 0

  def start(self):
    cmd = self.bin_path.split()
    self.proc = subprocess.Popen(
      cmd,
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      text=True,
      bufsize=1
    )
    self._initialize()

  def _send(self, method, params=None, is_notification=False):
    self.msg_id += 1
    msg = {
      "jsonrpc": "2.0",
      "method": method
    }
    if params is not None:
      msg["params"] = params
    if not is_notification:
      msg["id"] = self.msg_id

    payload = json.dumps(msg)
    self.proc.stdin.write(payload + "\n")
    self.proc.stdin.flush()
    return self.msg_id

  def _recv(self, expected_id=None):
    while True:
      line = self.proc.stdout.readline()
      if not line:
        raise EOFError("MCP server process closed connection unexpectedly.")
      try:
        msg = json.loads(line)
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
      self.proc.stdin.close()
      try:
        self.proc.wait(timeout=5)
      except subprocess.TimeoutExpired:
        self.proc.kill()

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
      "final_observation": session["observation"]
    }
  finally:
    client.close()

if __name__ == "__main__":
  campaign = sys.argv[1] if len(sys.argv) > 1 else "stabilization-v1"
  play_session(campaign)
