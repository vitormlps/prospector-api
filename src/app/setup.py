#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ### Local deps
from .routers._api_router import get_api_router
from .utils.exception_handlers import http_exc_handler, generic_exc_handler
from .utils.writers import make_dirs
# from security.authentication import set_auth_provider
from .database.connection import set_db_connection
from .helpers import Logger


def setup_app(settings):
    app = FastAPI(root_path=settings.ROOT_PATH)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.exception_handler(HTTPException)(http_exc_handler)
    app.exception_handler(Exception)(generic_exc_handler)

    app.include_router(get_api_router())

    # set_auth_provider(settings)

    return app


def setup_database(settings):
    set_db_connection(settings.ENV, settings.POSTGRES_URI)

    # if settings.SQLALCHEMY_AUTOINIT:
    #     with database() as db:
    #         db.initialize_database()


def setup_helpers(settings):
    Logger.setup_logger(settings.APP_NAME, settings.ENV)

    make_dirs(settings.OUTPUT_FILES_PATH)
    make_dirs(settings.EXTRACTED_FILES_PATH)
