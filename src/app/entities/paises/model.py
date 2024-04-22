#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy.orm import relationship, Mapped, mapped_column, WriteOnlyMapped

# ### Local deps
from ..base.model import Base
from ..estabelecimentos.model import Estabelecimento
from ..socios.model import Socio


class Pais(Base):
    codigo: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    descricao: Mapped[str] = mapped_column(nullable=False)

    # socios = relationship("Socio", back_populates="pais", lazy="subquery")
    socios: WriteOnlyMapped["Socio"] = relationship("Socio", lazy="subquery")

    # estabelecimentos = relationship("Estabelecimento", back_populates="pais", lazy="subquery")
    estabelecimentos: WriteOnlyMapped["Estabelecimento"] = relationship("Estabelecimento", lazy="subquery")
