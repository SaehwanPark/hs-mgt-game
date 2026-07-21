import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "gui" / "audio-cue-contract.mjs"
AUDIO = ROOT / "gui" / "audio.mjs"
HTML = ROOT / "gui" / "index.html"
PROOF = ROOT / "gui" / "audio-cue-proof.html"


def run_node(script):
    return subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class AudioCueContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = CONTRACT.read_text(encoding="utf-8")
        cls.audio = AUDIO.read_text(encoding="utf-8")
        cls.html = HTML.read_text(encoding="utf-8")
        cls.proof = PROOF.read_text(encoding="utf-8")

    def test_all_sixteen_cues_have_complete_standards(self):
        result = run_node(
            """
            import { AUDIO_CUE_CONTRACT, AUDIO_CUE_POLICY, audioCueContractFor, validateAudioCueContracts } from './gui/audio-cue-contract.mjs';
            if (AUDIO_CUE_CONTRACT.schema_version !== 'audio-cue-contract-v1' || AUDIO_CUE_CONTRACT.entries.length !== 16) process.exit(1);
            if (validateAudioCueContracts().length || AUDIO_CUE_POLICY.normalization_gain !== 0.08 || AUDIO_CUE_POLICY.peak_ceiling_dbfs !== -3) process.exit(2);
            const ids = new Set(AUDIO_CUE_CONTRACT.entries.map((entry) => entry.id));
            for (const entry of AUDIO_CUE_CONTRACT.entries) {
              if (!ids.has(entry.id) || !entry.semantic_purpose || !entry.priority_class || !entry.duration_ms || !entry.text_equivalent || !entry.distinction || !entry.visible_trigger_source || entry.peak_ceiling_dbfs > -3) process.exit(3);
              if (audioCueContractFor(entry.id)?.id !== entry.id) process.exit(4);
            }
            if (audioCueContractFor('event.private-intent') !== null) process.exit(5);
            console.log(JSON.stringify({ count: AUDIO_CUE_CONTRACT.entries.length, priorities: [...new Set(AUDIO_CUE_CONTRACT.entries.map((entry) => entry.priority_class))] }));
            """
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(json.loads(result.stdout)["count"], 16)

    def test_runtime_decorates_cues_and_cues_only_preserves_cues(self):
        result = run_node(
            """
            import { AUDIO_CATALOG, cueEntry, createAudioClient } from './gui/audio.mjs';
            if (AUDIO_CATALOG.cues.length !== 16) process.exit(1);
            if (AUDIO_CATALOG.cues.some((entry) => !entry.semantic_purpose || !entry.priority_class || !entry.text_equivalent || entry.normalization_gain !== 0.08)) process.exit(2);
            const nodes = new Map();
            const root = {
              hidden: false,
              addEventListener() {},
              removeEventListener() {},
              querySelector(selector) {
                if (!nodes.has(selector)) nodes.set(selector, { value: '', checked: false, textContent: '', addEventListener() {}, setAttribute() {} });
                return nodes.get(selector);
              },
            };
            const client = createAudioClient({ root, AudioContextCtor: null });
            if (client.setMode('cues-only').mode !== 'cues-only' || client.state().mode !== 'cues-only') process.exit(3);
            if (client.setMode('unknown').ok) process.exit(4);
            if (client.setMusicState('pressure').state !== 'pressure') process.exit(5);
            if (client.playCue('ui.action-confirm').code !== 'visual_only') process.exit(6);
            if (cueEntry('event.operating-loss').peak_ceiling_dbfs !== -3) process.exit(7);
            client.destroy();
            console.log('pass');
            """
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(result.stdout.strip(), "pass")

    def test_proof_and_live_control_keep_audio_optional_and_visible_only(self):
        for marker in (
            "audio-cue-contract-v1",
            "semantic_purpose",
            "priority_class",
            "loudness_target_db",
            "peak_ceiling_dbfs",
            "normalization_gain",
            "text_equivalent",
            "distinction",
            "visible_trigger_source",
            "cues-only",
            "audio-mode",
            "AUDIO_CUE_CONTRACT",
            "validation errors",
        ):
            self.assertIn(marker, self.contract + self.audio + self.html + self.proof)
        for forbidden in (
            "CompetitiveWorldState",
            "resolved_inputs",
            "effect_queue",
            "private_rival",
            "fetch(",
            "WebSocket",
            "Math.random",
        ):
            self.assertNotIn(forbidden, self.contract + self.audio + self.proof)
        for path in (CONTRACT, AUDIO):
            result = subprocess.run(
                ["node", "--check", str(path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
