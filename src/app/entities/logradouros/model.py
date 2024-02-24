#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List

# ### Third-party deps
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base
from ...utils.type_vars import TypeVars


class Logradouro(Base):
    tipo: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    nome_cidade_exterior: Mapped[str] = mapped_column(nullable=True)
    numero: Mapped[str] = mapped_column(nullable=True)
    complemento: Mapped[str] = mapped_column(nullable=True)
    bairro: Mapped[str] = mapped_column(nullable=True)
    cep: Mapped[str] = mapped_column(nullable=False)

    pais_id: Mapped[UUID] = mapped_column(ForeignKey("pais.id"), nullable=True)
    pais: Mapped[TypeVars.Pais] = relationship(back_populates="logradouros", lazy="subquery")

    municipio_id: Mapped[UUID] = mapped_column(ForeignKey("municipio.id"), nullable=False)
    municipio: Mapped[TypeVars.Municipio] = relationship(back_populates="logradouros", lazy="subquery")

    estabelecimentos: Mapped[List[TypeVars.Estabelecimento]] = relationship(back_populates="logradouro", lazy="subquery")
