from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

clients = []
mobile_clients = []
cloud_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            # Broadcast to all clients
            for client in clients:
                await client.send_text(data)

    except WebSocketDisconnect:
        clients.remove(websocket)

# ☁️ CLOUD SOCKET (sends data)
@app.websocket("/ws/mobile")
async def cloud_socket(websocket: WebSocket):
    await websocket.accept()
    cloud_clients.append(websocket)
    print("☁️ Cloud connected")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"☁️ Received from cloud: {data}")

            # 🚀 Send to all mobile clients
            disconnected = []
            for client in mobile_clients:
                try:
                    await client.send_text(data)
                except:
                    disconnected.append(client)

            # Cleanup dead connections
            for client in disconnected:
                mobile_clients.remove(client)

    except WebSocketDisconnect:
        cloud_clients.remove(websocket)
        print("☁️ Cloud disconnected")
