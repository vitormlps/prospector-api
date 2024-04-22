#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy.orm import relationship, Mapped, mapped_column, WriteOnlyMapped

# ### Local deps
from ..base.model import Base
from ..logradouros.model import Logradouro


class Municipio(Base):
    codigo: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    descricao: Mapped[str] = mapped_column(nullable=False)

    # logradouros = relationship("Logradouro", back_populates="municipio", lazy="subquery")
    logradouros: WriteOnlyMapped["Logradouro"] = relationship("Logradouro", lazy="subquery")
