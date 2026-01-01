import asyncio
import time
import random

# ------------------------------------
# ASYNC I/O SIMULATIONS
# ------------------------------------
async def download_file(name):
    print(f"📥 Downloading {name}")
    await asyncio.sleep(2)
    print(f"✅ Downloaded {name}")
    return f"{name} downloaded"


async def send_email(email):
    print(f"📧 Sending email to {email}")
    await asyncio.sleep(1)

    # simulate random failure
    if random.choice([True, False]):
        raise RuntimeError(f"Email failed for {email}")

    print(f"✅ Email sent to {email}")
    return f"Email sent to {email}"


async def fetch_data(api):
    print(f"🌐 Fetching data from {api}")
    await asyncio.sleep(3)
    print(f"✅ Data fetched from {api}")
    return f"Data from {api}"


# ------------------------------------
# SEQUENTIAL EXECUTION
# ------------------------------------
async def sequential():
    print("\n=== SEQUENTIAL EXECUTION ===")
    start = time.time()

    try:
        await download_file("video.mp4")
        await send_email("user@example.com")
        await fetch_data("api.service.com")
    except Exception as e:
        print("❌ Error:", e)

    print(f"Sequential time: {time.time() - start:.2f} seconds")


# ------------------------------------
# CONCURRENT EXECUTION
# ------------------------------------
async def concurrent():
    print("\n=== CONCURRENT EXECUTION ===")
    start = time.time()

    # schedule coroutines
    tasks = [
        asyncio.create_task(download_file("video.mp4")),
        asyncio.create_task(send_email("user@example.com")),
        asyncio.create_task(fetch_data("api.service.com"))
    ]

    # run in parallel + handle exceptions
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, Exception):
            print("❌ Task error:", result)
        else:
            print("✅ Result:", result)

    print(f"Concurrent time: {time.time() - start:.2f} seconds")


# ------------------------------------
# MAIN EVENT LOOP
# ------------------------------------
async def main():
    await sequential()
    await concurrent()

asyncio.run(main())
