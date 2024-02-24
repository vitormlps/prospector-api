#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List

# ### Third-party deps
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base
from ...utils.type_vars import TypeVars


class Socio(Base):
    nome: Mapped[str] = mapped_column(nullable=False)
    cpf_cnpj: Mapped[str] = mapped_column(nullable=True)
    data_entrada_sociedade: Mapped[DateTime] = mapped_column(nullable=False)

    empresa_id: Mapped[UUID] = mapped_column(ForeignKey("empresa.id"), nullable=False, index=True)
    empresa: Mapped[TypeVars.Empresa] = relationship(back_populates="socios", lazy="subquery")

    qualificacao_id: Mapped[UUID] = mapped_column(ForeignKey("qualificacao.id"), nullable=False)
    qualificacao: Mapped[TypeVars.Qualificacao] = relationship(lazy="subquery")

    representante_legal_id: Mapped[UUID] = mapped_column(ForeignKey("representante_legal.id"), nullable=False)
    representante_legal: Mapped[TypeVars.RepresentanteLegal] = relationship(lazy="subquery")

    pais_id: Mapped[UUID] = mapped_column(ForeignKey("pais.id"))
    pais: Mapped[TypeVars.Pais] = relationship(lazy="subquery")

    faixa_etaria_id: Mapped[UUID] = mapped_column(ForeignKey("faixa_etaria.id"))
    faixa_etaria: Mapped[TypeVars.FaixaEtaria] = relationship(lazy="subquery")
