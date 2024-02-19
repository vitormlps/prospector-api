#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from fastapi import HTTPException
from starlette.responses import JSONResponse

# ### Local deps


async def http_exc_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


async def generic_exc_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )


def throw_auth_error(msg: str):
    raise HTTPException(
            status_code=401,
            detail=msg,
            headers={'WWW-Authenticate': 'Bearer'}
    )