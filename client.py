import asyncio
import websockets

async def chat():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as websocket:
        print("🟢 Connected to server")

        loop = asyncio.get_running_loop()

        async def send():
            while True:
                # move blocking input to thread
                msg = await loop.run_in_executor(None, input, "You: ")
                await websocket.send(msg)

        async def receive():
            async for message in websocket:
                print(f"\n📩 Broadcast: {message}")

        await asyncio.gather(send(), receive())

asyncio.run(chat())
