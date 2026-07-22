import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "gui" / "asset-availability.mjs"
FACILITIES = ROOT / "gui" / "facility-components.mjs"
IDENTITIES = ROOT / "gui" / "identity-kits.mjs"
PROOF = ROOT / "gui" / "asset-fallback-proof.html"


class AssetFallbackTests(unittest.TestCase):
  def test_availability_and_presentation_outcomes_are_explicit(self):
    script = r"""
      import { assetPresentationFor, normalizeAssetAvailability } from './gui/asset-availability.mjs';
      import { facilityPresentationFor } from './gui/facility-components.mjs';
      import { identityPresentationFor } from './gui/identity-kits.mjs';
      const asset = { id: 'hospital', label: 'General hospital', source: 'Visible facility', equivalent: 'Hospital label', release_path: 'assets/release/hospital.svg', fallback: { id: 'generic', label: 'Facility', equivalent: 'Hospital label; generic marker' } };
      const loaded = assetPresentationFor(asset, { ok: true });
      const missing = assetPresentationFor(asset, undefined);
      const failed = assetPresentationFor(asset, false);
      const malformed = assetPresentationFor(asset, { status: 'unexpected' });
      const contradictory = [
        assetPresentationFor(asset, { ok: true, status: 'failed' }),
        assetPresentationFor(asset, { ok: true, reason: 'missing' }),
        assetPresentationFor(asset, { ok: false, status: 'loaded' }),
        assetPresentationFor(asset, { status: 'loaded', reason: 'missing' }),
      ];
      const typedMalformed = [
        assetPresentationFor(asset, { ok: 'false', status: 'loaded' }),
        assetPresentationFor(asset, { ok: true, status: 7 }),
        assetPresentationFor(asset, { status: 'loaded', reason: 7 }),
      ];
      const facility = facilityPresentationFor('general-hospital-base', 'missing');
      const identity = identityPresentationFor('northlake', { ok: false, reason: 'failed' });
      const unknownFacility = facilityPresentationFor('unknown-facility', 'missing');
      const unknownIdentity = identityPresentationFor('unknown-institution', 'missing');
      if (normalizeAssetAvailability('loaded').status !== 'loaded') process.exit(1);
      if (normalizeAssetAvailability(null).status !== 'missing') process.exit(2);
      if (normalizeAssetAvailability(false).status !== 'failed') process.exit(3);
      if (normalizeAssetAvailability({ status: 'malformed' }).status !== 'malformed') process.exit(4);
      if (loaded.display_mode !== 'asset' || loaded.release_path !== asset.release_path) process.exit(5);
      for (const outcome of [missing, failed, malformed, facility, identity]) {
        if (outcome.display_mode !== 'fallback' || outcome.release_path !== null || !outcome.requested_label || !outcome.equivalent) process.exit(6);
      }
      for (const outcome of contradictory) {
        if (outcome.asset_status !== 'malformed' || outcome.display_mode !== 'fallback' || outcome.release_path !== null) process.exit(9);
      }
      for (const outcome of typedMalformed) {
        if (outcome.asset_status !== 'malformed' || outcome.display_mode !== 'fallback' || outcome.release_path !== null) process.exit(10);
      }
      if (facility.requested_label !== 'General hospital base' || identity.requested_label !== 'Northlake') process.exit(7);
      if (unknownFacility.rendered_label !== 'Facility' || unknownFacility.equivalent !== 'Facility label and generic marker') process.exit(11);
      if (unknownIdentity.rendered_label !== 'Institution' || unknownIdentity.equivalent !== 'Institution identity unavailable') process.exit(12);
      if (JSON.stringify({ loaded, missing, facility, identity }).match(/CompetitiveWorldState|resolved_inputs|private_rival|effect_queue|Math\.random|fetch\(|WebSocket/)) process.exit(8);
      console.log('asset fallback contract passed');
    """
    result = subprocess.run(["node", "--input-type=module", "-e", script], cwd=ROOT, capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_proof_is_accessible_and_has_no_external_or_authority_boundary(self):
    content = PROOF.read_text(encoding="utf-8")
    for marker in ("lang=\"en\"", "aria-labelledby=\"title\"", "aria-live=\"polite\"", "Written equivalent", "Not used in fallback"):
      self.assertIn(marker, content)
    for forbidden in ("fetch(", "WebSocket", "CompetitiveWorldState", "resolved_inputs", "private_rival", "effect_queue", "Math.random"):
      self.assertNotIn(forbidden, content)

  def test_javascript_syntax_is_valid(self):
    for path in (MODULE, FACILITIES, IDENTITIES):
      result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True, check=False)
      self.assertEqual(result.returncode, 0, f"{path}: {result.stderr}")


if __name__ == "__main__":
  unittest.main()
