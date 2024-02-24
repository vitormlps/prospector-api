#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel

# ### Local deps


# class BaseSchema(BaseModel):
#     id: UUID
#     created_at: datetime
#     updated_at: datetime


class DefaultQueryFilter(BaseModel):
    unit_id: int
    skip: Optional[int]
    limit: Optional[int]
