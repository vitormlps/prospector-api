#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel, Field

# ### Local deps


class VersionamentosBase(BaseModel):
    rf_last_update: str = Field(min_length=19, max_length=19)


class VersionamentosCreate(VersionamentosBase):
    pass


class VersionamentosUpdate(VersionamentosBase):
    id: UUID
    rf_last_update: str = Field(min_length=19, max_length=19)


class VersionamentosView(VersionamentosBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
