#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from fastapi import HTTPException
from fastapi.websockets import WebSocketDisconnect

# ### Local deps
from ..security.current_user_auth import get_current_user


def websocket_auth(token: str):
    try:
        return get_current_user(token)

    except HTTPException as err:
        raise WebSocketDisconnect(err.status_code)
