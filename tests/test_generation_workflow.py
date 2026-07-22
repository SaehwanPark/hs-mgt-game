import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "assets" / "generation" / "generation-workflow.json"
MODELS = ROOT / "assets" / "generation" / "approved-models.json"
MANIFEST = ROOT / "assets" / "generation" / "generation-manifest.json"
RECORDS = ROOT / "assets" / "generation" / "records"
PROMPTS = ROOT / "assets" / "generation" / "prompt-templates.json"
CHECKLIST = ROOT / "assets" / "generation" / "human-review-checklist.json"
CAPTURE = ROOT / "scripts" / "capture_generation_metadata.py"
VALIDATE = ROOT / "scripts" / "validate_generation_metadata.py"
PROOF = ROOT / "gui" / "generation-workflow-proof.html"


def run(command):
  return subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)


class GenerationWorkflowTests(unittest.TestCase):
  def test_workflow_registry_and_empty_manifest_validate(self):
    result = run(["python3", str(VALIDATE)])
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    workflow = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    models = json.loads(MODELS.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    self.assertEqual(workflow["schema_version"], "generation-workflow-v1")
    self.assertEqual(models["entries"][0]["model_license"], "Apache-2.0")
    self.assertTrue(models["entries"][0]["model_card_url"].startswith("https://huggingface.co/"))
    self.assertEqual(manifest["entries"], [])

  def test_capture_hashes_complete_pending_record_and_validation_fails_closed(self):
    human_fields = json.loads(CHECKLIST.read_text(encoding="utf-8"))["required_checks"]
    with tempfile.TemporaryDirectory(dir=RECORDS) as directory:
      temp = Path(directory)
      source = temp / "source.bin"
      source.write_bytes(b"deterministic source output")
      source_relative = source.relative_to(ROOT).as_posix()
      request = {
        "asset_id": "future.test-portrait",
        "asset_type": "visual",
        "semantic_role": "identity",
        "model_id": "black-forest-labs.flux-1-schnell",
        "model_name": "black-forest-labs/FLUX.1-schnell",
        "model_version": "FLUX.1-schnell",
        "model_revision": "741f7c3ce8b383c54771c7003378a50191e9efe9",
        "model_license": "Apache-2.0",
        "model_card_url": "https://huggingface.co/black-forest-labs/FLUX.1-schnell",
        "generation_application": "local test harness",
        "prompt": "fictional editorial test portrait",
        "negative_prompt": "real person, logo, watermark",
        "seed": 42,
        "sampler": "test-sampler",
        "settings": {"steps": 4, "guidance_scale": 0},
        "dimensions": {"width": 512, "height": 512},
        "generation_date": "2026-07-21",
        "contributor": "test contributor",
        "post_processing": "none",
        "source_image_references": [],
        "accessible_equivalent": "Fictional test portrait; generic identity marker fallback.",
        "source_output_path": source_relative,
        "human_review": {entry["id"]: False for entry in human_fields},
        "approval_status": "pending",
        "asset_registry_id": None,
      }
      request_path = temp / "request.json"
      output_path = temp / "record.json"
      request_path.write_text(json.dumps(request), encoding="utf-8")
      captured = run(["python3", str(CAPTURE), "capture", "--request", str(request_path), "--output", str(output_path)])
      self.assertEqual(captured.returncode, 0, captured.stderr + captured.stdout)
      record = json.loads(output_path.read_text(encoding="utf-8"))
      self.assertTrue(record["source_hash"].startswith("sha256:"))
      checked = run(["python3", str(CAPTURE), "validate", "--record", str(output_path)])
      self.assertEqual(checked.returncode, 0, checked.stderr + checked.stdout)
      record["schema_version"] = "wrong-schema"
      output_path.write_text(json.dumps(record), encoding="utf-8")
      invalid_schema = run(["python3", str(CAPTURE), "validate", "--record", str(output_path)])
      self.assertNotEqual(invalid_schema.returncode, 0)
      self.assertIn("schema_version", invalid_schema.stderr)
      record["schema_version"] = "generation-record-v1"
      output_path.write_text(json.dumps(record), encoding="utf-8")
      source.write_bytes(b"mutated source output")
      mismatched = run(["python3", str(CAPTURE), "validate", "--record", str(output_path)])
      self.assertNotEqual(mismatched.returncode, 0)
      self.assertIn("source_hash", mismatched.stderr)

      record["approval_status"] = "approved"
      source.write_bytes(b"deterministic source output")
      output_path.write_text(json.dumps(record), encoding="utf-8")
      unreviewed = run(["python3", str(CAPTURE), "validate", "--record", str(output_path)])
      self.assertNotEqual(unreviewed.returncode, 0)
      self.assertIn("human review", unreviewed.stderr)

      record["approval_status"] = "pending"
      record["model_revision"] = "wrong-revision"
      output_path.write_text(json.dumps(record), encoding="utf-8")
      wrong_model_revision = run(["python3", str(CAPTURE), "validate", "--record", str(output_path)])
      self.assertNotEqual(wrong_model_revision.returncode, 0)
      self.assertIn("model_revision", wrong_model_revision.stderr)

      record["model_revision"] = "741f7c3ce8b383c54771c7003378a50191e9efe9"
      record["asset_id"] = "visual.runtime-resolution-sequence"
      record["asset_registry_id"] = "visual.runtime-resolution-sequence"
      output_path.write_text(json.dumps(record), encoding="utf-8")
      mismatched_registry = run(["python3", str(CAPTURE), "validate", "--record", str(output_path)])
      self.assertNotEqual(mismatched_registry.returncode, 0)
      self.assertIn("linked registry", mismatched_registry.stderr)

      outside_output = Path(tempfile.gettempdir()) / "hs-mgt-generation-record.json"
      outside = run(["python3", str(CAPTURE), "capture", "--request", str(request_path), "--output", str(outside_output)])
      self.assertNotEqual(outside.returncode, 0)
      self.assertIn("output_path", outside.stderr)

      existing_output = temp / "existing.json"
      existing_output.write_text("preserve me", encoding="utf-8")
      existing = run(["python3", str(CAPTURE), "capture", "--request", str(request_path), "--output", str(existing_output)])
      self.assertNotEqual(existing.returncode, 0)
      self.assertIn("refusing to overwrite", existing.stderr)
      self.assertEqual(existing_output.read_text(encoding="utf-8"), "preserve me")

  def test_unknown_model_and_incomplete_capture_are_rejected(self):
    with tempfile.TemporaryDirectory(dir=RECORDS) as directory:
      temp = Path(directory)
      source = temp / "source.bin"
      source.write_bytes(b"source")
      request = {"asset_id": "bad", "source_output_path": source.relative_to(ROOT).as_posix(), "model_id": "unknown"}
      request_path = temp / "request.json"
      request_path.write_text(json.dumps(request), encoding="utf-8")
      result = run(["python3", str(CAPTURE), "capture", "--request", str(request_path), "--output", str(temp / "record.json")])
      self.assertNotEqual(result.returncode, 0)
      self.assertIn("missing field", result.stderr)

  def test_proof_and_templates_keep_review_boundaries_visible(self):
    content = "\n".join(path.read_text(encoding="utf-8") for path in (WORKFLOW, MODELS, MANIFEST, PROMPTS, CHECKLIST, PROOF))
    for marker in (
      "generation-workflow-v1",
      "approved-generation-models-v1",
      "generation-manifest-v1",
      "model_revision",
      "negative_prompt",
      "source_hash",
      "release_hash",
      "real_person_resemblance_reviewed",
      "logo_trademark_reviewed",
      "clinical_plausibility_reviewed",
      "asset_registry_id",
      "no_model_weights_in_repository",
      "no_hosted_inference_dependency",
      "Fixture-only proof",
      "Release blocked",
    ):
      self.assertIn(marker, content)
    self.assertNotIn("fetch(", PROOF.read_text(encoding="utf-8"))
    self.assertNotIn("WebSocket", PROOF.read_text(encoding="utf-8"))


if __name__ == "__main__":
  unittest.main()
