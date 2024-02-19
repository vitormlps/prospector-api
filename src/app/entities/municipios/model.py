#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import Column, String
# from sqlalchemy.orm import relationship

# ### Local deps
from ..base.model import Base


class Municipios(Base):
    codigo = Column(String(), nullable=False, unique=True)
    descricao = Column(String(), nullable=False, unique=True)

    # estabelecimentos = relationship("Estabelecimentos", back_populates="municipios", lazy="subquery")
    # socios = relationship("Socios", back_populates="municipios", lazy="subquery")
