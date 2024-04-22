#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel, Field

# ### Local deps
from ..cnaes.schema import CNAEsView
from ..matrizes_filiais.schema import MatrizesFiliaisView
from ..situacoes_cadastrais.schema import SituacoesCadastraisView
from ..motivos.schema import MotivosView
from ..paises.schema import PaisesView
from ..logradouros.schema import LogradourosView
from ..contatos.schema import ContatosView
from ..base.schema import DefaultQueryFilter


class EstabelecimentosBase(BaseModel):
    cnpj_ordem: str = Field(min_length=4, max_length=4)
    cnpj_digit_verif: str = Field(min_length=2, max_length=2)
    nome_fantasia: Optional[str] = Field(min_length=3)
    data_situacao_cadastral: datetime
    data_inicio_atividade: datetime
    cnaes_secundarios: Optional[str]
    situacao_especial: Optional[str]
    data_situacao_especial: Optional[datetime]
    empresa_cnpj: str
    cnae_principal_id: UUID
    matriz_filial_id: UUID
    situacao_cadastral_id: UUID
    motivo_id: UUID
    pais_id: UUID
    logradouro_id: UUID


class EstabelecimentosCreate(EstabelecimentosBase):
    pass


class EstabelecimentosUpdate(EstabelecimentosBase):
    id: UUID
    cnpj_ordem: Optional[str] = Field(min_length=4, max_length=4)
    cnpj_digit_verif: Optional[str] = Field(min_length=2, max_length=2)
    data_situacao_cadastral: Optional[datetime]
    data_inicio_atividade: Optional[datetime]
    empresa_cnpj: Optional[str]
    cnae_principal_id: Optional[UUID]
    matriz_filial_id: Optional[UUID]
    situacao_cadastral_id: Optional[UUID]
    motivo_id: Optional[UUID]
    pais_id: Optional[UUID]
    logradouro_id: Optional[UUID]


class EstabelecimentosView(EstabelecimentosBase):
    id: UUID
    cnpj_ordem: str
    cnpj_digit_verif: str
    nome_fantasia: Optional[str]
    # cnae_principal: CNAEsView
    # matriz_filial: MatrizesFiliaisView
    # situacao_cadastral: SituacoesCadastraisView
    # motivo: MotivosView
    pais_id: Optional[UUID]
    # pais: PaisesView
    # logradouro: LogradourosView
    # contatos: List[ContatosView]
    created_at: datetime
    updated_at: datetime

    # def dict(self, **kwargs):
    #     kwargs['exclude'] = {'cnae_principal_id', 'matriz_filial_id', 'situacao_cadastral_id', 'motivo_id', 'logradouro_id', 'pais_id'}
    #     return super().dict(**kwargs)

    # def json(self, **kwargs):
    #     kwargs['exclude'] = {'cnae_principal_id', 'matriz_filial_id', 'situacao_cadastral_id', 'motivo_id', 'logradouro_id', 'pais_id'}
    #     return super().json(**kwargs)

    class Config:
        orm_mode = True


class EstabelecimentosFilter(DefaultQueryFilter):
    cnpj_ordem: Optional[str]
    cnpj_digit_verif: Optional[str]
    data_situacao_cadastral: Optional[datetime]
    data_inicio_atividade: Optional[datetime]
    empresa_cnpj: Optional[str]
    cnae_principal_id: Optional[UUID]
    matriz_filial_id: Optional[UUID]
    situacao_cadastral_id: Optional[UUID]
    motivo_id: Optional[UUID]
    pais_id: Optional[UUID]
    logradouro_id: Optional[UUID]