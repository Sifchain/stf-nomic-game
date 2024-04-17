import json
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

# List to hold all active WebSocket connections
connections: List[WebSocket] = []


@router.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        await websocket.send_text("Welcome to the Nomic game WebSocket!")
        while True:
            data = await websocket.receive_text()
            # Process incoming messages assuming they are JSON strings with an event type
            message = json.loads(data)
            event_type = message.get("event_type")

            # print message
            print(f"Received message: {message}")

            # print event_type
            print(f"Received event_type: {event_type}")

    except WebSocketDisconnect:
        connections.remove(websocket)
        print("WebSocket disconnected")
        await broadcast_message("A player has disconnected.")


async def broadcast_message(message: str):
    for connection in connections:
        await connection.send_text(message)
