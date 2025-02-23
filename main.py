from fastapi import FastAPI, WebSocket
import redis
import json
from game_logic import TexasHoldemGame

app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

game = TexasHoldemGame()

clients = {}

@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await websocket.accept()
    clients[player_id] = websocket
    await broadcast(f"🎮 {player_id} joined the table!")

    try:
        while True:
            data = await websocket.receive_text()
            action = json.loads(data)

            response = game.process_action(player_id, action)
            redis_client.publish("poker_game", json.dumps(response))
            await broadcast(response)

    except Exception:
        del clients[player_id]
        await broadcast(f"❌ {player_id} left the table!")

async def broadcast(message):
    for ws in clients.values():
        await ws.send_text(json.dumps({"message": message}))
