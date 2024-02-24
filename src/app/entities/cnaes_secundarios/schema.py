#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel

# ### Local deps
from ..estabelecimentos.schema import EstabelecimentosView
from ..cnaes.schema import CNAEsView


class CNAEsSecundariosBase(BaseModel):
    estabelecimento_id: UUID
    cnae_id: UUID


class CNAEsSecundariosCreate(CNAEsSecundariosBase):
    pass


class CNAEsSecundariosUpdate(CNAEsSecundariosBase):
    id: int
    estabelecimento_id: Optional[UUID]
    cnae_id: Optional[UUID]


class CNAEsSecundariosView(CNAEsSecundariosBase):
    id: int
    estabelecimento: EstabelecimentosView
    cnae: CNAEsView
    created_at: datetime
    updated_at: datetime

    def dict(self, **kwargs):
        kwargs['exclude'] = {'estabelecimento_id', 'cnae_id'}
        return super().dict(**kwargs)

    def json(self, **kwargs):
        kwargs['exclude'] = {'estabelecimento_id', 'cnae_id'}
        return super().json(**kwargs)

    class Config:
        orm_mode = True
