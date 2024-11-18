from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Wait for the client to send a message
            data = await websocket.receive_text()
            print(f"Received: {data}")

            # Echo the message back to the client
            response = f"Echo: {data}"
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print("Client disconnected")
