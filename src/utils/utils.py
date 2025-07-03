import random
import asyncio


async def time_sleep__by_user_info(min_delay: int = 2, max_delay: int = 5) -> int:
    delay = random.randint(min_delay, max_delay)
    await asyncio.sleep(delay)
    return delay


async def time_sleep__by_user_stories(min_delay: int = 3, max_delay: int = 6) -> int:
    delay = random.randint(min_delay, max_delay)
    await asyncio.sleep(delay)
    return delay