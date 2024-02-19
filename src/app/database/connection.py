#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Generator

# ### Third-party deps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ### Local deps


class Database:
    engine = None
    local_session = None


def set_database_engine(env, db_uri):
    if env != "development":
        Database.engine = create_engine(
            db_uri, 
            pool_pre_ping=True, 
            pool_recycle=60, 
            ignore_no_transaction_on_rollback=True
        )
    else:
        Database.engine = create_engine(
            db_uri, 
            pool_pre_ping=True, 
            ignore_no_transaction_on_rollback=True, 
            isolation_level="AUTOCOMMIT"
        )


def set_db_local_session():
    Database.local_session = sessionmaker(autocommit=False, autoflush=False, bind=Database.engine)


def set_db_connection(env, db_uri):
    set_database_engine(env, db_uri)
    set_db_local_session()


def get_db_local_session() -> Generator:
    with Database.local_session() as session:
        yield session
