import importlib.util
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "gui" / "index.html"
APP = ROOT / "gui" / "app.mjs"
RENDERER = ROOT / "gui" / "asset-credits-renderer.mjs"
RUNTIME = ROOT / "gui" / "asset-credits.mjs"


def load_module(name, relative_path):
  spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
  module = importlib.util.module_from_spec(spec)
  assert spec.loader is not None
  spec.loader.exec_module(module)
  return module


CREDITS = load_module("generate_asset_credits", "scripts/generate_asset_credits.py")


class InGameCreditsTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.html = HTML.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")
    cls.renderer = RENDERER.read_text(encoding="utf-8")
    cls.runtime = RUNTIME.read_text(encoding="utf-8")

  def test_runtime_projection_is_generated_from_canonical_registries(self):
    self.assertEqual(CREDITS.render_runtime(ROOT), self.runtime)
    result = subprocess.run(
      [
        "node", "--input-type=module", "-e",
        "import { ASSET_CREDITS } from './gui/asset-credits.mjs'; console.log(`${ASSET_CREDITS.schema_version}:${ASSET_CREDITS.entries.length}:${ASSET_CREDITS.third_party_release_count}`);",
      ],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "asset-credits-v1:45:0")

  def test_credits_surface_is_visible_and_accessible(self):
    for marker in (
      'id="asset-credits-disclosure"',
      'id="asset-credits-summary"',
      'id="asset-credits-list"',
      'id="asset-credits-limit"',
      "Asset credits and provenance",
      "Accessible equivalent",
      "Approval",
      "Source URL",
      "Retrieved",
      "License reference",
      "Release",
    ):
      self.assertIn(marker, self.html + self.renderer)
    self.assertIn("renderAssetCredits({ root: document })", self.app)
    self.assertIn('aria-label="Registered visual and audio asset credits"', self.html)

  def test_renderer_is_text_first_and_does_not_cross_authority_boundary(self):
    for forbidden in ("fetch(", "WebSocket", "innerHTML", "submitTurn", "transition_competitive", "resolved_inputs"):
      self.assertNotIn(forbidden, self.renderer)
    self.assertIn("textContent", self.renderer)
    self.assertIn("replaceChildren", self.renderer)
    self.assertNotIn("https://", self.html.lower())

  def test_renderer_handles_a_minimal_catalog_without_html_injection(self):
    script = r'''
      import { renderAssetCredits } from "./gui/asset-credits-renderer.mjs";
      const nodes = new Map([
        ["#asset-credits-summary", { textContent: "" }],
        ["#asset-credits-list", { children: [], replaceChildren() { this.children = []; }, append(...items) { this.children.push(...items); } }],
        ["#asset-credits-limit", { textContent: "" }],
      ]);
      const root = {
        querySelector(selector) { return nodes.get(selector); },
        createElement(tag) {
          return {
            tag,
            children: [],
            append(...items) { this.children.push(...items); },
            textContent: "",
            className: "",
          };
        },
      };
      const result = renderAssetCredits({
        root,
        catalog: {
          third_party_release_count: 0,
          entries: [{
            id: "fixture.asset",
            asset_type: "visual",
            source: "fixture.svg",
            license: "project-generated",
            attribution: "Fixture attribution",
            approval_status: "approved",
            provenance: { kind: "repository-authored" },
            release_status: "not-released",
            accessible_equivalent: "Fixture text equivalent",
          }],
        },
      });
      console.log(`${result.ok}:${result.count}:${nodes.get("#asset-credits-list").children[0].children[0].textContent}`);
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "true:1:fixture.asset")


if __name__ == "__main__":
  unittest.main()
