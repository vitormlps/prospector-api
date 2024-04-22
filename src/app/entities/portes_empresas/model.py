#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy.orm import relationship, Mapped, mapped_column, WriteOnlyMapped

# ### Local deps
from ..base.model import Base
from ..empresas.model import Empresa


class PorteEmpresa(Base):
    codigo: Mapped[str] = mapped_column(nullable=False, unique=True)
    descricao: Mapped[str] = mapped_column(nullable=False)

    # empresas = relationship("Empresa", back_populates="porte_empresa", lazy="subquery")
    empresas: WriteOnlyMapped["Empresa"] = relationship("Empresa", lazy="subquery")
