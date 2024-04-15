import pytest
import websockets


@pytest.mark.asyncio
async def test_websocket_connection():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        greeting = await websocket.recv()
        assert (
            greeting == "Welcome to the Nomic game WebSocket!"
        ), "Failed to receive correct welcome message"
