import json
from typing import Dict, List
from fastapi import WebSocket


class WSManager:
    def __init__(self):
        # sala_id -> list of (session_token, websocket)
        self._rooms: Dict[str, List[tuple]] = {}

    def _get_room(self, sala_id: str) -> List[tuple]:
        return self._rooms.setdefault(sala_id, [])

    async def connect(self, websocket: WebSocket, sala_id: str, session_token: str):
        await websocket.accept()
        room = self._get_room(sala_id)
        # Remove stale connection for same token
        self._rooms[sala_id] = [(t, ws) for t, ws in room if t != session_token]
        self._rooms[sala_id].append((session_token, websocket))

    def disconnect(self, websocket: WebSocket, sala_id: str):
        if sala_id in self._rooms:
            self._rooms[sala_id] = [(t, ws) for t, ws in self._rooms[sala_id] if ws is not websocket]

    async def broadcast(self, sala_id: str, payload: dict):
        message = json.dumps(payload)
        dead = []
        for token, ws in self._get_room(sala_id):
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)
        if dead:
            self._rooms[sala_id] = [(t, ws) for t, ws in self._rooms[sala_id] if ws not in dead]

    async def send_to(self, sala_id: str, session_token: str, payload: dict):
        message = json.dumps(payload)
        for token, ws in self._get_room(sala_id):
            if token == session_token:
                try:
                    await ws.send_text(message)
                except Exception:
                    pass
                return

    def connected_tokens(self, sala_id: str) -> List[str]:
        return [t for t, _ in self._get_room(sala_id)]


manager = WSManager()
