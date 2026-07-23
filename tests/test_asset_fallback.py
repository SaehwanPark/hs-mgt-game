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

  def test_every_registered_facility_and_identity_has_fallback_coverage(self):
    script = r"""
      import fs from 'node:fs';
      import { assetPresentationFor } from './gui/asset-availability.mjs';
      import { FACILITY_COMPONENTS, facilityPresentationFor } from './gui/facility-components.mjs';
      import { IDENTITY_KITS, identityPresentationFor } from './gui/identity-kits.mjs';

      const registry = JSON.parse(fs.readFileSync('./assets/registry/visual-assets.json', 'utf8'));
      const registryPaths = new Set(registry.entries.map((entry) => entry.release_path).filter(Boolean));
      const facilities = Object.entries(FACILITY_COMPONENTS).filter(([, component]) => component.release_path);
      const identities = Object.entries(IDENTITY_KITS).filter(([, kit]) => kit.asset.release_path);
      const catalogPaths = new Set([
        ...facilities.map(([, component]) => component.release_path),
        ...identities.map(([, kit]) => kit.asset.release_path),
      ]);
      if (catalogPaths.size !== registryPaths.size || [...catalogPaths].some((path) => !registryPaths.has(path))) process.exit(20);
      const outcomes = [];
      for (const [id, component] of facilities) {
        if (!component.fallback?.id || !component.fallback?.label || !component.fallback?.equivalent) process.exit(21);
        outcomes.push(...[null, false, { status: 'malformed' }, { status: 'loaded', reason: 'missing' }].map((availability) => facilityPresentationFor(id, availability)));
      }
      for (const [id, kit] of identities) {
        if (!kit.fallback?.id || !kit.fallback?.label || !kit.fallback?.equivalent) process.exit(22);
        outcomes.push(...[null, false, { status: 'malformed' }, { status: 'loaded', reason: 'missing' }].map((availability) => identityPresentationFor(id, availability)));
      }
      for (const outcome of outcomes) {
        if (outcome.display_mode !== 'fallback' || outcome.release_path !== null || !outcome.equivalent || !outcome.fallback_reason) process.exit(23);
      }
      const direct = assetPresentationFor({ id: 'registered', label: 'Registered', release_path: 'assets/release/registered.svg', fallback: { id: 'generic', label: 'Generic', equivalent: 'Written generic equivalent' } }, null);
      if (direct.display_mode !== 'fallback' || direct.release_path !== null || direct.equivalent !== 'Written generic equivalent') process.exit(24);
      if (JSON.stringify(outcomes).match(/CompetitiveWorldState|resolved_inputs|private_rival|effect_queue|Math\.random|fetch\(|WebSocket/)) process.exit(25);
      console.log(JSON.stringify({ facilities: facilities.length, identities: identities.length, registry: registryPaths.size, outcomes: outcomes.length }));
    """
    result = subprocess.run(["node", "--input-type=module", "-e", script], cwd=ROOT, capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), '{"facilities":12,"identities":3,"registry":15,"outcomes":60}')

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
