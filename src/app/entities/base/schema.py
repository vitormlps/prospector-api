#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel, Field

# ### Local deps


class DefaultQueryFilter(BaseModel):
    id: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    skip: Optional[int] = 0
    limit: Optional[int] = 0


class BaseFilter(DefaultQueryFilter):
    codigo: Optional[str]
    descricao: Optional[str]
