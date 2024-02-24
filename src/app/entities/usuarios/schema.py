#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel, Field, EmailStr

# ### Local deps
from ..permissoes.schema import PermissoesView


class UsuariosBase(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=8)
    is_active: bool
    permissoes_id: UUID


class UsuariosCreate(UsuariosBase):
    pass


class UsuariosUpdate(UsuariosBase):
    id: UUID
    first_name: Optional[str] = Field(min_length=3)
    last_name: Optional[str] = Field(min_length=2)
    email: Optional[EmailStr]
    password: Optional[str] = Field(min_length=8)
    permissoes_id: Optional[UUID]


class UsuariosView(UsuariosBase):
    permissoes: PermissoesView
    created_at: datetime
    updated_at: datetime

    def dict(self, **kwargs):
        kwargs['exclude'] = {'permissoes_id', 'password'}
        return super().dict(**kwargs)

    def json(self, **kwargs):
        kwargs['exclude'] = {'permissoes_id', 'password'}
        return super().json(**kwargs)

    class Config:
        orm_mode = True
