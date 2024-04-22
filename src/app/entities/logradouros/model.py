#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, WriteOnlyMapped
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base
from ..estabelecimentos.model import Estabelecimento


class Logradouro(Base):
    tipo: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    numero: Mapped[str] = mapped_column(nullable=True)
    complemento: Mapped[str] = mapped_column(nullable=True)
    bairro: Mapped[str] = mapped_column(nullable=True)
    cep: Mapped[str] = mapped_column(nullable=False)
    estado_uf: Mapped[str] = mapped_column(nullable=False)

    municipio_id: Mapped[UUID] = mapped_column(ForeignKey("municipio.id"), nullable=False)
    # municipio = relationship("Municipio", back_populates="logradouros", lazy="subquery")

    # estabelecimentos = relationship("Estabelecimento", back_populates="logradouro", lazy="subquery")
    estabelecimentos: WriteOnlyMapped["Estabelecimento"] = relationship("Estabelecimento", lazy="subquery")
