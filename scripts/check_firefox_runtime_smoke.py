#!/usr/bin/env python3
"""Run a bounded Firefox/Marionette smoke check against a loopback GUI host."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import socket
import subprocess
import tempfile
import time
from pathlib import Path
from urllib.parse import urlparse


DEFAULT_URL = "http://127.0.0.1:7878/"
DEFAULT_PORT = 2828
LOOPBACK_HOSTS = {"127.0.0.1", "::1"}
EXPECTED_PAGE_TITLE = "Health Policy Strategy Game — Executive Desktop"
FIREFOX_CANDIDATES = (
  "/Applications/Firefox.app/Contents/MacOS/firefox",
  "/usr/bin/firefox",
  "/usr/local/bin/firefox",
)


def _packet_bytes(payload: object) -> bytes:
  data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
  return str(len(data)).encode("ascii") + b":" + data


class MarionetteClient:
  def __init__(self, host: str, port: int, timeout: float = 15.0):
    self.socket = socket.create_connection((host, port), timeout=timeout)
    self.socket.settimeout(timeout)
    self.message_id = 0

  def close(self) -> None:
    self.socket.close()

  def _receive(self) -> object:
    header = bytearray()
    while b":" not in header:
      part = self.socket.recv(1)
      if not part:
        raise RuntimeError("Firefox Marionette closed before sending a packet")
      header.extend(part)
    length = int(header[:-1])
    data = bytearray()
    while len(data) < length:
      part = self.socket.recv(length - len(data))
      if not part:
        raise RuntimeError("Firefox Marionette closed during a packet")
      data.extend(part)
    return json.loads(data.decode("utf-8"))

  def command(self, name: str, parameters: dict) -> object:
    self.message_id += 1
    self.socket.sendall(_packet_bytes([0, self.message_id, name, parameters]))
    response = self._receive()
    if not isinstance(response, list) or len(response) < 4:
      raise RuntimeError(f"unexpected Marionette response: {response!r}")
    if response[0] != 1 or response[1] != self.message_id:
      raise RuntimeError(f"unexpected Marionette response ID: {response!r}")
    if response[2] is not None:
      raise RuntimeError(response[2])
    return response[3]


def _find_firefox(explicit: str | None) -> str:
  candidates = [explicit] if explicit else []
  candidates.extend(FIREFOX_CANDIDATES)
  for candidate in candidates:
    if candidate and Path(candidate).is_file():
      return candidate
  discovered = shutil.which("firefox")
  if discovered:
    return discovered
  raise RuntimeError("Firefox executable not found")


def _validate_loopback_url(url: str) -> None:
  parsed = urlparse(url)
  if parsed.scheme not in {"http", "https"} or parsed.hostname not in LOOPBACK_HOSTS:
    raise RuntimeError("runtime smoke URL must use an HTTP(S) loopback host")
  if parsed.username or parsed.password:
    raise RuntimeError("runtime smoke URL must not include credentials")


def validate_observations(
  shell: object,
  host: object,
  url: str,
  browser: object,
  marionette_protocol: object,
) -> None:
  if not isinstance(shell, dict) or not isinstance(host, dict) or not isinstance(browser, dict):
    raise RuntimeError("Firefox runtime smoke observations must be objects")
  runtime_errors = []
  if marionette_protocol != 3:
    runtime_errors.append("Firefox Marionette protocol is not version 3")
  if browser.get("name") != "firefox":
    runtime_errors.append("browser identity is not Firefox")
  if not isinstance(browser.get("version"), str) or not browser["version"].strip():
    runtime_errors.append("Firefox browser version is missing")
  if not isinstance(browser.get("platform"), str) or not browser["platform"].strip():
    runtime_errors.append("Firefox platform capability is missing")
  if browser.get("headless") is not True:
    runtime_errors.append("Firefox headless capability is missing")
  if runtime_errors:
    raise RuntimeError("; ".join(runtime_errors))
  shell_errors = []
  if shell.get("title") != EXPECTED_PAGE_TITLE:
    shell_errors.append("page title does not match the executive desktop shell")
  if shell.get("url") != url:
    shell_errors.append("shell URL does not match the requested loopback URL")
  if shell.get("ready") != "complete":
    shell_errors.append("document did not reach readyState=complete")
  if shell.get("start_control") is not True:
    shell_errors.append("session-start control is missing")
  if shell.get("demo_fixture") is not True:
    shell_errors.append("demo fixture was not present before host start")
  if shell_errors:
    raise RuntimeError("; ".join(shell_errors))

  host_errors = []
  status = host.get("status")
  if not isinstance(status, str) or not status.startswith("competitive regional session loaded: "):
    host_errors.append("host did not report a competitive regional session load")
  session = host.get("session")
  if not isinstance(session, str) or not re.fullmatch(r"session-[A-Za-z0-9_-]+", session):
    host_errors.append("host did not return a non-empty opaque session ID")
  if host.get("demo_fixture") is not False:
    host_errors.append("demo fixture remained present after host start")
  if host_errors:
    raise RuntimeError("; ".join(host_errors))


def _wait_for_port(host: str, port: int, timeout: float) -> None:
  deadline = time.monotonic() + timeout
  while time.monotonic() < deadline:
    try:
      with socket.create_connection((host, port), timeout=0.5):
        return
    except OSError:
      time.sleep(0.1)
  raise RuntimeError(f"Firefox Marionette did not open {host}:{port}")


def _execute(client: MarionetteClient, session_id: str, script: str) -> object:
  result = client.command(
    "WebDriver:ExecuteScript",
    {"sessionId": session_id, "script": script, "args": []},
  )
  return result.get("value") if isinstance(result, dict) else result


def run_probe(url: str = DEFAULT_URL, firefox_bin: str | None = None) -> dict:
  _validate_loopback_url(url)
  firefox = _find_firefox(firefox_bin)
  with tempfile.TemporaryDirectory(prefix="hs-firefox-runtime-") as profile:
    process = subprocess.Popen(
      [
        firefox,
        "--headless",
        "--new-instance",
        "--profile",
        profile,
        "--marionette",
        "--remote-allow-hosts",
        "127.0.0.1",
        url,
      ],
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT,
      text=True,
    )
    client = None
    session_id = None
    try:
      _wait_for_port("127.0.0.1", DEFAULT_PORT, 15.0)
      client = MarionetteClient("127.0.0.1", DEFAULT_PORT)
      hello = client._receive()
      created = client.command(
        "WebDriver:NewSession",
        {"capabilities": {"alwaysMatch": {"browserName": "firefox"}, "firstMatch": []}},
      )
      session_id = created["sessionId"]
      capabilities = created["capabilities"]
      client.command("WebDriver:Navigate", {"sessionId": session_id, "url": url})
      time.sleep(0.5)
      shell = _execute(client, session_id, """
        return {
          title: document.title,
          ready: document.readyState,
          start_control: Boolean(document.querySelector('#session-start')),
          demo_fixture: document.body.innerText.includes('Demo fixture loaded'),
          url: location.href
        };
      """)
      _execute(client, session_id, "document.querySelector('#session-start').click(); return true;")
      time.sleep(1.0)
      host = _execute(client, session_id, """
        return {
          status: document.querySelector('#session-launch-status')?.textContent || '',
          session: document.querySelector('#session-id')?.value || '',
          demo_fixture: document.body.innerText.includes('Demo fixture loaded')
        };
      """)
      browser = {
        "name": capabilities.get("browserName"),
        "version": capabilities.get("browserVersion"),
        "platform": capabilities.get("platformName"),
        "headless": capabilities.get("moz:headless"),
      }
      validate_observations(shell, host, url, browser, hello.get("marionetteProtocol"))
      client.command("WebDriver:DeleteSession", {"sessionId": session_id})
      session_id = None
      return {
        "status": "pass",
        "url": url,
        "marionette_protocol": hello.get("marionetteProtocol"),
        "browser": browser,
        "shell": shell,
        "host_start": host,
      }
    finally:
      if client is not None:
        if session_id is not None:
          try:
            client.command("WebDriver:DeleteSession", {"sessionId": session_id})
          except (OSError, RuntimeError):
            pass
        client.close()
      if process.poll() is None:
        process.terminate()
        try:
          process.wait(timeout=5)
        except subprocess.TimeoutExpired:
          process.kill()
          process.wait(timeout=5)


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--url", default=DEFAULT_URL)
  parser.add_argument("--firefox-bin")
  args = parser.parse_args()
  try:
    print(json.dumps(run_probe(args.url, args.firefox_bin), indent=2, sort_keys=True))
  except (OSError, RuntimeError, TimeoutError, KeyError, TypeError) as error:
    print(json.dumps({"status": "fail", "errors": [str(error)]}, indent=2, sort_keys=True))
    return 1
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
