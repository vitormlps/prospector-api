#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import inspect

# ### Third-party deps
from fastapi import APIRouter

# ### Local deps
from app import routers

def get_routers():
    return list(filter(lambda x: inspect.ismodule(x[1]), inspect.getmembers(routers)))

def get_api_router():
    api_routes = get_routers()
    
    api_router = APIRouter()
    [api_router.include_router(router[1].router) for router in api_routes]

    return api_router

