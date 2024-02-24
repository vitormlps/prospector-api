#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List

# ### Third-party deps
from sqlalchemy.orm import relationship, Mapped, mapped_column

# ### Local deps
from ..base.model import Base
from ...utils.type_vars import TypeVars


class Pais(Base):
    codigo: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    nome: Mapped[str] = mapped_column(nullable=False)

    logradouros: Mapped[List[TypeVars.Logradouro]] = relationship(back_populates="pais", lazy="subquery")

    socios: Mapped[List[TypeVars.Socio]] = relationship(back_populates="pais", lazy="subquery")
