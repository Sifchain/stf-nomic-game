import asyncio

import websockets


async def test_websocket():
    uri = "ws://localhost:8000/ws"

    async with websockets.connect(uri) as websocket:
        # Wait for the welcome message
        greeting = await websocket.recv()
        print(f"Received from server: {greeting}")

        # Receive and print messages from the server
        try:
            while True:
                message = await websocket.recv()
                print(f"Received from server: {message}")
        except websockets.ConnectionClosed:
            print("WebSocket connection closed")


asyncio.run(test_websocket())
