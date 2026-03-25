from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

mobile_clients = []
cloud_clients = []


# 📱 MOBILE SOCKET (receives data)
@app.websocket("/ws/mobile")
async def mobile_socket(websocket: WebSocket):
    await websocket.accept()
    mobile_clients.append(websocket)
    print("📱 Mobile connected")

    try:
        while True:
            # Optional: receive messages from mobile if needed
            await websocket.receive_text()
    except WebSocketDisconnect:
        mobile_clients.remove(websocket)
        print("📱 Mobile disconnected")


# ☁️ CLOUD SOCKET (sends data)
@app.websocket("/ws/cloud")
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
