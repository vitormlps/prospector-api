#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List

# ### Third-party deps
from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base
from ...utils.type_vars import TypeVars


class Estabelecimento(Base):
    cnpj_ordem: Mapped[str] = mapped_column(String(4), nullable=False)
    cnpj_digit_verif: Mapped[str] = mapped_column(String(2), nullable=False)
    nome_fantasia: Mapped[str] = mapped_column(nullable=True)
    data_situacao_cadastral: Mapped[DateTime] = mapped_column(nullable=False)
    data_inicio_atividade: Mapped[DateTime] = mapped_column(nullable=False)
    situacao_especial: Mapped[str] = mapped_column(nullable=True)
    data_situacao_especial: Mapped[DateTime] = mapped_column(nullable=True)

    empresa_id: Mapped[UUID] = mapped_column(ForeignKey("empresa.id"), nullable=False, index=True)
    empresa: Mapped[TypeVars.Empresa] = relationship(back_populates="estabelecimentos", lazy="subquery")

    cnae_principal_id: Mapped[UUID] = mapped_column(ForeignKey("cnae.id"), nullable=False)
    cnae_principal: Mapped[TypeVars.CNAE] = relationship(lazy="subquery")

    cnaes_secundarios: Mapped[List[TypeVars.CNAEsSecundarios]] = relationship(back_populates="estabelecimento", lazy="subquery")

    matriz_filial_id: Mapped[UUID] = mapped_column(ForeignKey("matriz_filial.id"), nullable=False)
    matriz_filial: Mapped[TypeVars.MatrizFilial] = relationship(lazy="subquery")

    situacao_cadastral_id: Mapped[UUID] = mapped_column(ForeignKey("situacao_cadastral.id"), nullable=False)
    situacao_cadastral: Mapped[TypeVars.SituacaoCadastral] = relationship(lazy="subquery")

    motivo_id: Mapped[UUID] = mapped_column(ForeignKey("motivo.id"), nullable=False)
    motivo: Mapped[TypeVars.Motivo] = relationship(lazy="subquery")

    logradouro_id: Mapped[UUID] = mapped_column(ForeignKey("logradouro.id"), nullable=False)
    logradouro: Mapped[TypeVars.Logradouro] = relationship(back_populates="estabelecimentos", lazy="subquery")
    
    contatos: Mapped[List[TypeVars.Contato]] = relationship(back_populates="estabelecimento", lazy="subquery")
