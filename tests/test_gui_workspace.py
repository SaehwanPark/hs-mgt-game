import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "gui" / "workspace.mjs"
HTML = ROOT / "gui" / "index.html"
APP = ROOT / "gui" / "app.mjs"


class GuiWorkspaceTests(unittest.TestCase):
  def test_event_mapping_and_density_contract(self):
    script = r'''
      import { DEFAULT_VISIBLE_COUNTS, WORKSPACE_IDS, workspaceForEvent } from "./gui/workspace.mjs";
      const expected = ["setup", "brief", "decide", "resolve", "review"];
      if (JSON.stringify(WORKSPACE_IDS) !== JSON.stringify(expected)) process.exit(1);
      if (workspaceForEvent("session_loaded") !== "brief") process.exit(2);
      if (workspaceForEvent({ type: "session_loaded", done: true }) !== "review") process.exit(3);
      if (workspaceForEvent("briefing_reviewed") !== "decide") process.exit(4);
      if (workspaceForEvent("transition_committed") !== "resolve") process.exit(5);
      if (workspaceForEvent("resolution_continued") !== "brief") process.exit(6);
      if (DEFAULT_VISIBLE_COUNTS.signals !== 3 || DEFAULT_VISIBLE_COUNTS.actions !== 6 || DEFAULT_VISIBLE_COUNTS.history !== 5) process.exit(7);
      console.log("ok");
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

  def test_controller_hides_inactive_workspaces_and_marks_current_navigation(self):
    script = r'''
      import { createWorkspaceController } from "./gui/workspace.mjs";
      function node(id, workspace) {
        return {
          id, dataset: { workspace }, hidden: false, attributes: {}, focused: false,
          setAttribute(name, value) { this.attributes[name] = value; },
          removeAttribute(name) { delete this.attributes[name]; },
          querySelector() { return { focus: () => { this.focused = true; } }; },
          addEventListener() {},
        };
      }
      const setup = node("workspace-setup", "setup");
      const brief = node("workspace-brief", "brief");
      const decide = node("workspace-decide", "decide");
      const navBrief = { dataset: { workspaceNav: "true", workspaceTarget: "brief" }, attributes: {}, setAttribute(n, v) { this.attributes[n] = v; }, removeAttribute(n) { delete this.attributes[n]; }, addEventListener() {} };
      const navDecide = { dataset: { workspaceNav: "true", workspaceTarget: "decide" }, attributes: {}, setAttribute(n, v) { this.attributes[n] = v; }, removeAttribute(n) { delete this.attributes[n]; }, addEventListener() {} };
      const root = {
        activeElement: null,
        querySelectorAll(selector) {
          if (selector === "[data-workspace]") return [setup, brief, decide];
          if (selector === "[data-workspace-area]") return [];
          if (selector === "[data-workspace-areas]") return [];
          if (selector === "[data-workspace-nav]") return [navBrief, navDecide];
          if (selector === "[data-workspace-target]") return [];
          if (selector === "[data-dialog-target]") return [];
          if (selector === "[data-dialog-close]") return [];
          if (selector === "dialog") return [];
          return [];
        },
        querySelector(selector) {
          return { "[data-workspace=setup]": setup, "[data-workspace=brief]": brief, "[data-workspace=decide]": decide }[selector] ?? null;
        },
      };
      const controller = createWorkspaceController({ root });
      if (setup.hidden || !brief.hidden || !decide.hidden) process.exit(1);
      controller.setWorkspace("decide", { focus: false });
      if (decide.hidden || !brief.hidden || !navDecide.attributes["aria-current"] || navBrief.attributes["aria-current"]) process.exit(2);
      console.log("ok");
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

  def test_module_parses(self):
    result = subprocess.run(["node", "--check", str(WORKSPACE)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_visible_information_rows_preserve_word_sized_wraps(self):
    html = HTML.read_text(encoding="utf-8")
    self.assertIn("overflow-wrap:break-word", html)
    self.assertIn("grid-template-columns:max-content minmax(0,1fr) minmax(8rem,1fr)", html)
    self.assertIn("grid-template-columns:repeat(2,1fr)", html)
    self.assertIn(".visual-token--marker .visual-token-label{white-space:nowrap}", html)
    self.assertIn(".timeline-row>.status{flex-basis:100%}", html)

  def test_long_actor_status_is_plain_text_not_a_badge(self):
    app = APP.read_text(encoding="utf-8")
    self.assertIn("heading.append(title);", app)
    self.assertIn("status.textContent = `• ${actor.status ?? \"Status unavailable\"}`;", app)


if __name__ == "__main__":
  unittest.main()
