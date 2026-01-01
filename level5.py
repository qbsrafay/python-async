import asyncio
import signal
import time
from concurrent.futures import ThreadPoolExecutor

# -------------------------------------------------
# ASYNC CONTEXT MANAGER (Resource handling)
# -------------------------------------------------
class AsyncResource:
    async def __aenter__(self):
        print("🔌 Resource acquired")
        await asyncio.sleep(0.2)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("🔌 Resource released")
        await asyncio.sleep(0.2)


# -------------------------------------------------
# ASYNC GENERATOR (Streaming data)
# -------------------------------------------------
async def data_stream():
    for i in range(10):
        await asyncio.sleep(0.5)
        yield f"frame-{i}"


# -------------------------------------------------
# PRODUCER
# -------------------------------------------------
async def producer(queue: asyncio.Queue):
    async with AsyncResource():
        async for item in data_stream():
            print(f"📤 Produced: {item}")
            await queue.put(item)

    # signal consumers to stop
    for _ in range(2):
        await queue.put(None)


# -------------------------------------------------
# CPU-BOUND WORK (Threaded)
# -------------------------------------------------
def cpu_bound_work(data):
    time.sleep(1)  # heavy computation simulation
    return data.upper()


# -------------------------------------------------
# CONSUMER
# -------------------------------------------------
async def consumer(name, queue: asyncio.Queue, executor):
    loop = asyncio.get_running_loop()

    try:
        while True:
            item = await queue.get()

            if item is None:
                print(f"🛑 {name} shutting down")
                break

            print(f"📥 {name} received: {item}")

            # offload CPU-bound work to thread
            result = await loop.run_in_executor(
                executor, cpu_bound_work, item
            )

            print(f"⚙️ {name} processed: {result}")
            queue.task_done()

    except asyncio.CancelledError:
        print(f"❌ {name} cancelled")
        raise


# -------------------------------------------------
# GRACEFUL SHUTDOWN HANDLER
# -------------------------------------------------
async def shutdown(signal_name, tasks):
    print(f"\n🚨 Received {signal_name}. Shutting down...")
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    print("✅ Shutdown complete")


# -------------------------------------------------
# MAIN ORCHESTRATION
# -------------------------------------------------
async def main():
    queue = asyncio.Queue(maxsize=5)
    executor = ThreadPoolExecutor(max_workers=2)

    prod = asyncio.create_task(producer(queue))
    cons1 = asyncio.create_task(consumer("Consumer-1", queue, executor))
    cons2 = asyncio.create_task(consumer("Consumer-2", queue, executor))

    tasks = [prod, cons1, cons2]

    # Windows-compatible signal handling
    def signal_handler(signum, frame):
        print(f"\n🚨 Received signal {signum}. Shutting down...")
        for task in tasks:
            task.cancel()
    
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)

    await asyncio.gather(*tasks, return_exceptions=True)
    executor.shutdown(wait=True)


# -------------------------------------------------
# EVENT LOOP
# -------------------------------------------------
asyncio.run(main())
