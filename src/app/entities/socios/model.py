#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from datetime import datetime

# ### Third-party deps
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base


class Socio(Base):
    nome: Mapped[str] = mapped_column(nullable=False)
    cpf_cnpj: Mapped[str] = mapped_column(nullable=True)
    data_entrada_sociedade: Mapped[datetime] = mapped_column(nullable=False)

    empresa_cnpj: Mapped[str] = mapped_column(ForeignKey("empresa.cnpj_basico"), nullable=False, index=True)
    # empresa = relationship("Empresa", back_populates="socios", lazy="subquery")

    qualificacao_id: Mapped[UUID] = mapped_column(ForeignKey("qualificacao.id"), nullable=False)
    # qualificacao = relationship("Qualificacao", back_populates="socios", lazy="subquery")

    pais_id: Mapped[UUID] = mapped_column(ForeignKey("pais.id"), nullable=True)
    # pais = relationship("Pais", back_populates="socios", lazy="subquery")

    representante_legal_id: Mapped[UUID] = mapped_column(ForeignKey("representante_legal.id"), nullable=True)
    # representante_legal = relationship("RepresentanteLegal", back_populates="socios", lazy="subquery")

    faixa_etaria_id: Mapped[UUID] = mapped_column(ForeignKey("faixa_etaria.id"), nullable=True)
    # faixa_etaria = relationship("FaixaEtaria", back_populates="socios", lazy="subquery")
