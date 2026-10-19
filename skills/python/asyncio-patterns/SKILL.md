---
name: asyncio-patterns
description: Production asynchronous programming with Asyncio, TaskGroups, timeouts, and concurrency throttling. Use when developing async servers, background workers, event loops, and handling cancellation.
---

# Production Asyncio Patterns (Python 3.11+)

Architect reliable, high-throughput, non-blocking asynchronous Python workflows.

## 1. Structured Concurrency with `TaskGroup`

Avoid unmanaged `asyncio.create_task` dangling references. Use `TaskGroup` for structured concurrency:

```python
import asyncio

async def fetch_item(item_id: int) -> str:
    await asyncio.sleep(0.1)
    return f"Item {item_id}"

async def process_batch(ids: list[int]) -> list[str]:
    results: list[str] = []
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch_item(i)) for i in ids]
    return [t.result() for t in tasks]
```

## 2. Enforcing Timeouts

Use `asyncio.timeout` for deterministic deadline management:

```python
async def fetch_with_deadline(url: str) -> str:
    async with asyncio.timeout(5.0):
        return await call_remote_service(url)
```

## 3. Concurrency Limiting with `Semaphore`

Prevent overwhelming databases or external APIs with bounded concurrency:

```python
sem = asyncio.Semaphore(10)

async def throttled_fetch(url: str) -> bytes:
    async with sem:
        return await download(url)
```

## 4. Graceful Shutdown & Signal Handling

Always cancel pending tasks cleanly on SIGINT / SIGTERM:

```python
tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
for t in tasks:
    t.cancel()
await asyncio.gather(*tasks, return_exceptions=True)
```
