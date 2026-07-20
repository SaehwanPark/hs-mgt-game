import json
import unittest
import xml.etree.ElementTree as ElementTree
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SVG_ROOT = ROOT / "assets" / "source" / "visual" / "art-direction"
BOARD = ROOT / "docs" / "design" / "visual-audio-art-direction-board.md"
ADR = ROOT / "docs" / "decision-records" / "0012-visual-audio-art-direction.md"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"
CREDITS = ROOT / "assets" / "ASSET_CREDITS.md"


class VisualAudioArtDirectionTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.board = BOARD.read_text(encoding="utf-8")
    cls.adr = ADR.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    cls.credits = CREDITS.read_text(encoding="utf-8")

  def test_three_reference_variants_are_well_formed_and_accessible(self):
    variants = sorted(SVG_ROOT.glob("variant-*.svg"))
    self.assertEqual([path.stem for path in variants], [
      "variant-a-institutional",
      "variant-b-civic-terrain",
      "variant-c-editorial-desktop",
    ])
    for path in variants:
      root = ElementTree.parse(path).getroot()
      self.assertEqual(root.attrib.get("role"), "img")
      self.assertEqual(root.attrib.get("viewBox"), "0 0 960 600")
      self.assertIn("aria-labelledby", root.attrib)
      self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}title"))
      self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}desc"))
      text = " ".join(element.text or "" for element in root.iter())
      self.assertIn("Riverside", text)
      self.assertIn("constrained", text.lower())
      raw = path.read_text(encoding="utf-8")
      for forbidden in ("<image", "<script", "<foreignObject", "font-face", "href=", "url(", "https://"):
        self.assertNotIn(forbidden, raw)
      self.assertNotIn("http://", raw.replace('xmlns="http://www.w3.org/2000/svg"', ""))

  def test_scored_selection_and_rejections_are_recorded(self):
    for marker in (
      "Variant A — institutional flat executive board",
      "Variant B — civic terrain board (rejected)",
      "Variant C — editorial executive desktop (rejected)",
      "**29**",
      "**19**",
      "**24**",
      "Color-blind review",
      "Small-size review",
      "Large-text review",
      "Select Variant A",
      "unsupported geography risk",
      "dashboard-only risk",
    ):
      self.assertIn(marker, self.board)
    for marker in (
      "# ADR-0012",
      "Status:** Accepted",
      "Use the flat institutional direction",
      "Variant B, civic terrain: rejected",
      "Variant C, editorial desktop: rejected",
      "Native SVG",
      "not a geographic model",
    ):
      self.assertIn(marker, self.adr)

  def test_source_references_are_registered_and_credited(self):
    ids = {entry["id"] for entry in self.registry["entries"]}
    for suffix in ("a", "b", "c"):
      asset_id = f"visual.art-direction.variant-{suffix}"
      self.assertIn(asset_id, ids)
      self.assertIn(asset_id, self.credits)
    self.assertTrue(all(
      entry["release_path"] is None
      for entry in self.registry["entries"]
      if entry["id"].startswith("visual.art-direction.")
    ))

  def test_design_slice_does_not_expand_runtime_authority(self):
    combined = self.board + self.adr + "\n".join(
      path.read_text(encoding="utf-8") for path in SVG_ROOT.glob("variant-*.svg")
    ).replace("http://www.w3.org/2000/svg", "")
    for forbidden in (
      "CompetitiveWorldState", "resolved_inputs", "effect_queue", "transition_competitive",
      "fetch(", "WebSocket", "http://", "https://",
    ):
      self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
  unittest.main()
