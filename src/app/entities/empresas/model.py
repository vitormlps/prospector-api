#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, WriteOnlyMapped
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base
from ..estabelecimentos.model import Estabelecimento
from ..simples_nacional.model import SimplesNacional
from ..socios.model import Socio


class Empresa(Base):
    cnpj_basico: Mapped[str] = mapped_column(String(8), nullable=False, unique=True, index=True)
    razao_social: Mapped[str] = mapped_column(nullable=False)
    capital_social: Mapped[float] = mapped_column(nullable=False)

    natureza_juridica_id: Mapped[UUID] = mapped_column(ForeignKey("natureza_juridica.id"), nullable=False)
    # natureza_juridica = relationship("NaturezaJuridica", back_populates="empresas", lazy="subquery")

    qualificacao_responsavel_id: Mapped[UUID] = mapped_column(ForeignKey("qualificacao.id"), nullable=False)
    # qualificacao_responsavel = relationship("Qualificacao", back_populates="empresas", lazy="subquery")

    porte_empresa_id: Mapped[UUID] = mapped_column(ForeignKey("porte_empresa.id"), nullable=False)
    # porte_empresa = relationship("PorteEmpresa", back_populates="empresas", lazy='subquery')

    # simples_nacional = relationship("SimplesNacional", back_populates="empresa", lazy="subquery", cascade="all, delete-orphan")
    simples_nacional: WriteOnlyMapped["SimplesNacional"] = relationship("SimplesNacional", lazy="subquery", cascade="all, delete-orphan")

    # estabelecimentos = relationship("Estabelecimento", back_populates="empresa", lazy="subquery", cascade="all, delete-orphan")
    estabelecimentos: WriteOnlyMapped["Estabelecimento"] = relationship("Estabelecimento", lazy="subquery", cascade="all, delete-orphan")
    
    # socios = relationship("Socio", back_populates="empresa", lazy="subquery")
    socios: WriteOnlyMapped["Socio"] = relationship("Socio", lazy="subquery")
