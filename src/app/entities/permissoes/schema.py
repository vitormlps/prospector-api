#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel

# ### Local deps


class PermissoesBase(BaseModel):
    tipo: str
    can_view: bool
    can_update: bool
    can_delete: bool


class PermissoesCreate(PermissoesBase):
    pass


class PermissoesUpdate(PermissoesBase):
    id: UUID
    tipo: Optional[str]
    can_view: Optional[bool]
    can_update: Optional[bool]
    can_delete: Optional[bool]


class PermissoesView(PermissoesBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
