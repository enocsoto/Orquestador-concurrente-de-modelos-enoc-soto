"""Concurrent model fan-out, with a timeout and a concurrency cap."""

import asyncio
import logging
from collections.abc import Awaitable, Sequence

from orchestrator.calls import claude_3_call, gpt_4_call, local_llama_call

logger = logging.getLogger(__name__)

max_observed_concurrency = 0


async def query_models(
    calls: Sequence[Awaitable[str]] | None = None,
    timeout: float = 2.0,
) -> list[str] | None:
    """Query the models in parallel. Return None if the timeout expires."""
    if calls is None:
        calls = (gpt_4_call(), claude_3_call(), local_llama_call())
    try:
        async with asyncio.timeout(timeout):
            return list(await asyncio.gather(*calls))
    except TimeoutError:
        logger.error(
            "TimeoutError: se agotó el tiempo al consultar los modelos; se continúa"
        )
        return None


async def simulate_calls(n: int = 10, limit: int = 2, delay: float = 0.3) -> None:
    """Fire n calls and allow at most `limit` of them to run at once."""
    global max_observed_concurrency
    semaphore = asyncio.Semaphore(limit)
    in_flight = 0
    peak = 0

    async def _one(index: int) -> None:
        nonlocal in_flight, peak
        async with semaphore:
            in_flight += 1
            if in_flight > peak:
                peak = in_flight
            try:
                if in_flight > limit:
                    raise RuntimeError(
                        f"concurrency {in_flight} exceeds the limit {limit}"
                    )
                logger.info("inicio de la simulación %s", index)
                await asyncio.sleep(delay)
                logger.info("fin de la simulación %s", index)
            finally:
                in_flight -= 1

    await asyncio.gather(*(_one(index) for index in range(n)))
    max_observed_concurrency = peak


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    await query_models()
    await simulate_calls(10)


if __name__ == "__main__":
    asyncio.run(main())
