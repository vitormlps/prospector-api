#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy.orm import relationship, Mapped, mapped_column, WriteOnlyMapped

# ### Local deps
from ..base.model import Base
from ..socios.model import Socio


class FaixaEtaria(Base):
    codigo: Mapped[str] = mapped_column(nullable=False, unique=True)
    descricao: Mapped[str] = mapped_column(nullable=False)

    # socios = relationship("Socio", back_populates="faixa_etaria", lazy="subquery")
    socios: WriteOnlyMapped["Socio"] = relationship("Socio", lazy="subquery")
