#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List

# ### Third-party deps
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base
from ...utils.type_vars import TypeVars


class Empresa(Base):
    cnpj_basico: Mapped[str] = mapped_column(String(8), nullable=False, unique=True, index=True)
    razao_social: Mapped[str] = mapped_column(nullable=False)
    capital_social: Mapped[float] = mapped_column(Float, nullable=False)

    porte_empresa_id: Mapped[UUID] = mapped_column(ForeignKey("porte_empresa.id"), nullable=False)
    porte_empresa: Mapped[TypeVars.PorteEmpresa] = relationship(lazy='subquery')

    natureza_juridica_id: Mapped[UUID] = mapped_column(ForeignKey("natureza_juridica.id"), nullable=False)
    natureza_juridica: Mapped[TypeVars.NaturezaJuridica] = relationship(lazy="subquery")

    qualificacao_responsavel_id: Mapped[UUID] = mapped_column(ForeignKey("qualificacao_responsavel.id"), nullable=False)
    qualificacao_responsavel: Mapped[TypeVars.Qualificacao] = relationship(lazy="subquery")

    simples_nacional_id: Mapped[UUID] = mapped_column(ForeignKey("simples_nacional.id"), nullable=False)
    simples_nacional: Mapped[TypeVars.SimplesNacional] = relationship(back_populates="empresa", lazy="subquery")

    estabelecimentos: Mapped[List[TypeVars.Estabelecimento]] = relationship(back_populates="empresa", lazy="subquery")
    
    socios: Mapped[List[TypeVars.Socio]] = relationship(back_populates="empresa", lazy="subquery")
