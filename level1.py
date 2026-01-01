import time
import asyncio

# -------------------------------
# 1) SYNCHRONOUS (Blocking)
# -------------------------------
def sync_task(name):
    print(f"[SYNC] {name} started")
    time.sleep(2)   # blocks everything
    print(f"[SYNC] {name} finished")

print("=== SYNCHRONOUS EXECUTION ===")
start = time.time()
sync_task("Task 1")
sync_task("Task 2")
print(f"Synchronous time: {time.time() - start:.2f} seconds\n")


# -------------------------------
# 2) ASYNCHRONOUS (Non-blocking)
# -------------------------------
async def async_task(name):
    print(f"[ASYNC] {name} started")
    await asyncio.sleep(2)  # non-blocking wait
    print(f"[ASYNC] {name} finished")

# -------------------------------
# 3) SIMPLE COROUTINE
# -------------------------------
async def say_hello():
    print("Hello...")
    await asyncio.sleep(1)
    print("...World!")

# -------------------------------
# 4) EVENT LOOP SCHEDULING
# -------------------------------
async def main():
    await asyncio.gather(
        async_task("Task 1"),
        async_task("Task 2"),
        say_hello()
    )

print("=== ASYNCHRONOUS EXECUTION ===")
start = time.time()

# -------------------------------
# 5) RUN WITH asyncio.run()
# -------------------------------
asyncio.run(main())

print(f"Asynchronous time: {time.time() - start:.2f} seconds")
