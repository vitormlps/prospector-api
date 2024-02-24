#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List

# ### Third-party deps
from sqlalchemy.orm import relationship, Mapped, mapped_column

# ### Local deps
from ..base.model import Base
from ...utils.type_vars import TypeVars


class PorteEmpresa(Base):
    codigo: Mapped[str] = mapped_column(nullable=False, unique=True)
    descricao: Mapped[str] = mapped_column(nullable=False)

    empresas: Mapped[List[TypeVars.Empresa]] = relationship(back_populates="porte_empresa", lazy="subquery")
