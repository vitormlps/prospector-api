#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from datetime import datetime
from uuid import uuid4 as uuid

# ### Third-party deps
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

# ### Local deps
from app.utils.parsers import camel_to_snake


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)
    
    __INDEX_SEQUENCE = "index_sequence"

    __order_by = "created_at"
    __skip = 0
    __limit = 0

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, insert_default=uuid, unique=True)

    created_at: Mapped[datetime] = mapped_column(nullable=False, insert_default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, insert_default=datetime.now, onupdate=datetime.now)
