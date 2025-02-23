import asyncio
import websockets
import redis
import json

REDIS_HOST = "localhost"
REDIS_PORT = 6379

class PokerServer:
    def __init__(self):
        self.clients = {}
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    async def register(self, websocket, player_id):
        """Registers a new player connection."""
        self.clients[player_id] = websocket
        await self.broadcast(f"🎮 {player_id} joined the table!")

    async def unregister(self, player_id):
        """Removes a player on disconnect."""
        if player_id in self.clients:
            del self.clients[player_id]
            await self.broadcast(f"❌ {player_id} left the table!")

    async def broadcast(self, message):
        """Sends messages to all players."""
        for ws in self.clients.values():
            await ws.send(json.dumps({"message": message}))

    async def handle_message(self, websocket, message):
        """Processes incoming player actions."""
        data = json.loads(message)
        player_id = data.get("player_id")
        action = data.get("action")

        if action == "bet":
            amount = data.get("amount")
            await self.broadcast(f"💰 {player_id} bets {amount} chips!")

        elif action == "fold":
            await self.broadcast(f"🃏 {player_id} folds.")

        # Store actions in Redis for game state
        self.redis_client.publish("poker_actions", json.dumps(data))

    async def handler(self, websocket, path):
        """Main WebSocket handler."""
        try:
            player_id = await websocket.recv()
            await self.register(websocket, player_id)

            async for message in websocket:
                await self.handle_message(websocket, message)

        finally:
            await self.unregister(player_id)

# Start WebSocket Server
server = PokerServer()
start_server = websockets.serve(server.handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
