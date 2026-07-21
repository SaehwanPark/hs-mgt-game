import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "gui" / "resolution-sequence.mjs"
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"


def run_node(script):
    return subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class ResolutionSequenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = MODULE.read_text(encoding="utf-8")
        cls.app = APP.read_text(encoding="utf-8")
        cls.html = HTML.read_text(encoding="utf-8")

    def test_known_stages_have_stable_surface_and_audio_contract(self):
        result = run_node(
            """
            import { planResolutionSequence, sequenceFingerprint } from './gui/resolution-sequence.mjs';
            const envelope = {
              schema_version: 'competitive-resolution-v1',
              turn: 1,
              steps: [
                { id: 'submitted', source: 'command', items: ['hold'] },
                { id: 'responses', source: 'events', items: ['Payer response visible'] },
                { id: 'processes', source: 'projects', items: [] },
                { id: 'operations', source: 'operations', items: ['Margin: 12'] },
                { id: 'resources', source: 'resources', items: ['Cash: 60 → 48'] },
                { id: 'effects', source: 'effects', items: ['Beds changed by 10'] },
                { id: 'information', source: 'observation', items: ['Rival signal visible'] },
                { id: 'pending', source: 'pending', items: ['No pending process'] },
              ],
            };
            const sequence = planResolutionSequence(envelope);
            if (sequence.length !== 8) process.exit(1);
            if (sequence[0].stage_id !== 'submitted' || sequence[7].stage_id !== 'pending') process.exit(2);
            if (sequence[5].attention_priority >= sequence[0].attention_priority) process.exit(3);
            if (!sequence[1].surface_sync.includes('regional-board') || sequence[3].surface_sync[0] !== 'metric-summary') process.exit(4);
            if (sequence[1].audio_cue !== 'ui.report-received' || sequence[3].audio_cue !== 'ui.advance-month') process.exit(5);
            if (sequenceFingerprint(envelope) !== sequenceFingerprint(envelope)) process.exit(6);
            console.log(JSON.stringify(sequence.map(({ stage_id, attention_priority, surface_sync, audio_cue }) => ({ stage_id, attention_priority, surface_sync, audio_cue }))));
            """
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(len(json.loads(result.stdout)), 8)

    def test_missing_and_unknown_steps_remain_written_and_replay_stable(self):
        result = run_node(
            """
            import { planResolutionSequence, sequenceForReplay, sequenceForSkip } from './gui/resolution-sequence.mjs';
            const envelope = { steps: [{ id: 'responses', source: '', items: [] }, { id: 'future-host-stage', source: 'host', items: ['Visible extension'] }] };
            const sequence = planResolutionSequence(envelope, { reduced_motion: true });
            if (sequence.length !== 9 || sequence[0].items[0] !== 'Submitted batch unavailable.') process.exit(1);
            if (sequence[1].items[0] !== 'No visible institutional responses.') process.exit(2);
            if (sequence[8].stage_id !== 'future-host-stage' || sequence[8].present !== true) process.exit(3);
            if (sequence.some((entry) => !entry.items.length || !entry.reduced_motion)) process.exit(4);
            const skipped = sequenceForSkip(envelope);
            if (!skipped.skipped || !skipped.report_text_retained || skipped.written_stage_count !== 9) process.exit(5);
            if (JSON.stringify(sequenceForReplay(envelope)) !== JSON.stringify(sequenceForReplay(envelope))) process.exit(6);
            console.log('pass');
            """
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(result.stdout.strip(), "pass")

    def test_sequence_is_host_boundary_safe_and_keyboard_visible(self):
        for marker in (
            "planResolutionSequence",
            "sequenceForSkip",
            "audio_cue",
            "surface_sync",
            "priority_semantics",
            "resolution-next",
            "resolution-progress",
            "local pacing never removes committed text",
        ):
            self.assertIn(marker, self.module + self.app + self.html)
        for forbidden in (
            "transition_competitive",
            "resolved_inputs",
            "effect_queue",
            "Math.random",
            "fetch(",
            "WebSocket",
        ):
            self.assertNotIn(forbidden, self.module + self.app)
        for path in (MODULE, APP):
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
