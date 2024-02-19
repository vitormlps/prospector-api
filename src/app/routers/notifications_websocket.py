#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from fastapi import WebSocket, APIRouter
from starlette.websockets import WebSocketDisconnect

# ### Local deps
from ..middleware.websockets import websocket_auth


router = APIRouter()
connected_clients = dict()


@router.websocket("/notifications")
async def notification_events(websocket: WebSocket, token: str):
    user = websocket_auth(token)
    uuid = user.get("sub")
    session_state = user.get("session_state")
    try:
        connected_clients[session_state] = {
            "client": websocket,
            "uuid": uuid,
            "session_state": session_state,
        }
        await websocket.accept()

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        pass

    finally:
        await websocket.close()
        connected_clients.pop(session_state)


async def send_event(event, session_state: str):
    if session_state not in connected_clients:
        return
    client = connected_clients[session_state]

    client = client["client"]
    try:
        await client.send_json(event)
    except Exception as e:
        print(e)
