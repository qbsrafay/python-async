import asyncio
import aiohttp
import aiofiles
import aiosqlite
import time

DB_NAME = "data.db"
FILE_NAME = "response.txt"
URL = "https://jsonplaceholder.typicode.com/posts/1"


# -----------------------------------------
# 1) SIMULATE I/O-BOUND OPERATION
# -----------------------------------------
async def simulate_io():
    print("⏳ Simulating I/O work...")
    await asyncio.sleep(1)
    print("✅ I/O simulation done")


# -----------------------------------------
# 2) ASYNC HTTP REQUEST
# -----------------------------------------
async def download_data(session):
    print("🌐 Downloading data...")
    async with session.get(URL) as response:
        data = await response.text()
    print("✅ Download complete")
    return data


# -----------------------------------------
# 3) PROCESS DATA (CPU-LIGHT)
# -----------------------------------------
async def process_data(data):
    print("⚙️ Processing data...")
    await asyncio.sleep(0.5)  # simulate processing
    processed = data.upper()
    print("✅ Processing done")
    return processed


# -----------------------------------------
# 4) ASYNC FILE WRITE
# -----------------------------------------
async def save_to_file(data):
    print("💾 Saving to file...")
    async with aiofiles.open(FILE_NAME, "w") as f:
        await f.write(data)
    print("✅ File saved")


# -----------------------------------------
# 5) ASYNC DATABASE OPERATION
# -----------------------------------------
async def save_to_db(data):
    print("🗄️ Saving to database...")
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS responses (content TEXT)"
        )
        await db.execute(
            "INSERT INTO responses (content) VALUES (?)", (data,)
        )
        await db.commit()
    print("✅ Database saved")


# -----------------------------------------
# PIPELINE: DOWNLOAD → PROCESS → SAVE
# -----------------------------------------
async def pipeline():
    start = time.time()

    await simulate_io()

    async with aiohttp.ClientSession() as session:
        raw_data = await download_data(session)

    processed_data = await process_data(raw_data)

    # run file + DB saving concurrently
    await asyncio.gather(
        save_to_file(processed_data),
        save_to_db(processed_data)
    )

    print(f"\n⏱ Total time: {time.time() - start:.2f} seconds")


# -----------------------------------------
# EVENT LOOP
# -----------------------------------------
asyncio.run(pipeline())
