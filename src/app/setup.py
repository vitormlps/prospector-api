#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

# ### Local deps
from app.helpers import Logger
from .config import get_app_config
from .routers._api_router import get_api_router
from .utils.exception_handlers import http_exc_handler, generic_exc_handler
# from security.authentication import set_auth_provider
from .database.connection import set_db_connection, get_db_local_session
from .entities.base.repository import create_all


def setup_database(settings):
    logger = Logger().get_logger()
    set_db_connection(settings.ENV, settings.POSTGRES_URI)

    if settings.SQLALCHEMY_AUTOINIT:
        session = next(get_db_local_session())
        try:
            session.execute(text(
                f"SELECT 'CREATE DATABASE {settings.POSTGRES_DB}'\
                WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{settings.POSTGRES_DB}');"))
        except:
            logger.debug("Database already exists")

        create_all()


def setup_helpers(settings):
    Logger(settings.LOGGER_NAME, settings.LOG_DIR, settings.LOG_LEVEL)


def setup_app(settings = get_app_config()):
    setup_helpers(settings)
    setup_database(settings)

    app = FastAPI(root_path=settings.ROOT_PATH)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.exception_handler(HTTPException)(http_exc_handler)
    app.exception_handler(Exception)(generic_exc_handler)

    app.include_router(get_api_router())

    # set_auth_provider(settings)

    return app


app = setup_app()