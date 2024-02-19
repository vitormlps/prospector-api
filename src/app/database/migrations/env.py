#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import os
import sys
from logging.config import fileConfig

# ### Third-party deps
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from importlib import import_module
from alembic import context

# ### Local deps
from ...config import settings


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

from app.entities.base.model import Base


def auto_import_models() -> None:
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )

    base_path = os.path.abspath(os.path.join("entities"))

    if not os.path.exists(base_path):
        raise FileNotFoundError(
            f"O diretório especificado não foi encontrado: {base_path}"
        )

    model_modules = []

    for entity in os.listdir(base_path):
        entity_path = os.path.join(base_path, entity)

        if os.path.isdir(entity_path) and "model.py" in os.listdir(entity_path):
            model_module = f"entities.{entity}.model"
            model_modules.append(model_module)

    for model_module in sorted(model_modules):
        import_module(model_module)

        # Debugging
        print(f"ALEMBIC | Successfully imported module: {model_module}")


auto_import_models()

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string
    to the script output.
    """
    url = settings.DATABASE_URL
    print(url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    print(f"ALEMBIC | Migrations running in {url}")

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()

else:
    run_migrations_online()
