from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import redis
from app.config import REDIS_HOST

websocket_router = APIRouter(prefix="/ws", tags=["WebSockets"])
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

connections = {}

@websocket_router.websocket("/game/{room_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, player_id: str):
    await websocket.accept()
    connections[player_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            redis_client.publish(room_id, f"Player {player_id} says: {data}")
    except WebSocketDisconnect:
        del connections[player_id]
