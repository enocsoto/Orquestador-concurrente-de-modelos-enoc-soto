"""Tests for the concurrent orchestrator. Stdlib only."""

import asyncio
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from orchestrator import orchestrator as orch
from orchestrator.calls import claude_3_call, gpt_4_call, local_llama_call


class TestOrchestrator(unittest.TestCase):
    def test_source_has_no_time_sleep(self) -> None:
        files = list((ROOT / "orchestrator").rglob("*.py"))
        self.assertTrue(files)
        for file in files:
            text = file.read_text(encoding="utf-8")
            self.assertNotIn("time.sleep", text, file.name)

    def test_query_models_returns_results_when_they_fit_the_timeout(self) -> None:
        result = asyncio.run(
            orch.query_models(
                [
                    gpt_4_call(0.01),
                    claude_3_call(0.01),
                    local_llama_call(0.01),
                ],
                timeout=1.0,
            )
        )
        self.assertEqual(result, ["gpt-4", "claude-3", "local-llama"])

    def test_timeout_returns_none_without_propagating(self) -> None:
        async def slow() -> str:
            await asyncio.sleep(0.2)
            return "slow"

        async def fast(name: str) -> str:
            await asyncio.sleep(0.01)
            return name

        with self.assertLogs("orchestrator.orchestrator", level="ERROR") as logs:
            result = asyncio.run(
                orch.query_models(
                    [slow(), fast("a"), fast("b")],
                    timeout=0.05,
                )
            )

        self.assertIsNone(result)
        self.assertTrue(
            any("TimeoutError" in line and "continúa" in line for line in logs.output)
        )

    def test_semaphore_does_not_exceed_the_limit(self) -> None:
        asyncio.run(orch.simulate_calls(n=6, limit=2, delay=0.05))
        self.assertEqual(orch.max_observed_concurrency, 2)


if __name__ == "__main__":
    unittest.main()
