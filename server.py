import asyncio
import websockets

CONNECTED_CLIENTS = set()

async def handler(websocket):
    # Register client
    CONNECTED_CLIENTS.add(websocket)
    print(f"🟢 Client connected ({len(CONNECTED_CLIENTS)})")

    try:
        async for message in websocket:
            print(f"📨 Received: {message}")

            # Broadcast to all clients
            await asyncio.gather(
                *[client.send(message) for client in CONNECTED_CLIENTS]
            )

    except websockets.exceptions.ConnectionClosed:
        print("🔴 Client disconnected")

    finally:
        CONNECTED_CLIENTS.remove(websocket)
        print(f"🟡 Active clients: {len(CONNECTED_CLIENTS)}")


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("🚀 WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # run forever


asyncio.run(main())
