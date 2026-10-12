"""Coroutines that simulate network latency when calling models."""

import asyncio
import logging

logger = logging.getLogger(__name__)


async def gpt_4_call(delay: float = 0.6) -> str:
    logger.info("inicio de la llamada a gpt_4")
    await asyncio.sleep(delay)
    logger.info("fin de la llamada a gpt_4")
    return "gpt-4"


async def claude_3_call(delay: float = 1.2) -> str:
    logger.info("inicio de la llamada a claude_3")
    await asyncio.sleep(delay)
    logger.info("fin de la llamada a claude_3")
    return "claude-3"


async def local_llama_call(delay: float = 3.0) -> str:
    logger.info("inicio de la llamada a local_llama")
    await asyncio.sleep(delay)
    logger.info("fin de la llamada a local_llama")
    return "local-llama"
