import asyncio
import time

# ----------------------------------------
# SEMAPHORE (acts like a lock / limiter)
# ----------------------------------------
semaphore = asyncio.Semaphore(2)  # only 2 tasks allowed at a time


# ----------------------------------------
# LONG RUNNING I/O TASK
# ----------------------------------------
async def io_task(name, delay):
    async with semaphore:  # controlled access
        print(f"🔒 {name} acquired semaphore")
        try:
            await asyncio.sleep(delay)
            print(f"✅ {name} completed")
            return name
        finally:
            print(f"🔓 {name} released semaphore")


# ----------------------------------------
# TASK WITH TIMEOUT
# ----------------------------------------
async def task_with_timeout():
    try:
        return await asyncio.wait_for(io_task("TimeoutTask", 5), timeout=2)
    except asyncio.TimeoutError:
        print("⏰ Timeout occurred!")
        return "Timeout handled"


# ----------------------------------------
# DEPENDENT TASKS (Object A → Object B)
# ----------------------------------------
async def object_A():
    print("📦 Object A processing...")
    await asyncio.sleep(2)
    print("📦 Object A done")
    return "Data from A"


async def object_B(data):
    print(f"📨 Object B waiting for A's data: {data}")
    await asyncio.sleep(1)
    print("📨 Object B done")


# ----------------------------------------
# TASK CANCELLATION
# ----------------------------------------
async def cancellable_task():
    try:
        print("🚧 Cancellable task started")
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("❌ Task was cancelled!")
        raise


# ----------------------------------------
# MAIN ORCHESTRATION
# ----------------------------------------
async def main():
    start = time.time()

    # 1️⃣ Cancellation
    task = asyncio.create_task(cancellable_task())
    await asyncio.sleep(2)
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("🛑 Cancellation handled safely")

    # 2️⃣ Timeout handling
    result = await task_with_timeout()
    print("Timeout result:", result)

    # 3️⃣ Wait for one task before others start
    data_from_A = await object_A()  # must finish first
    await object_B(data_from_A)

    # 4️⃣ Multiple tasks with semaphore limiting concurrency
    tasks = [
        asyncio.create_task(io_task("Task-1", 3)),
        asyncio.create_task(io_task("Task-2", 3)),
        asyncio.create_task(io_task("Task-3", 3)),
        asyncio.create_task(io_task("Task-4", 3)),
    ]

    await asyncio.gather(*tasks)

    print(f"\n⏱ Total time: {time.time() - start:.2f} seconds")


# ----------------------------------------
# EVENT LOOP
# ----------------------------------------
asyncio.run(main())
