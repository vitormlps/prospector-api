#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

# ### Local deps
from ..base.model import Base


class Permissoes(Base):
    name = Column(String(), nullable=False)

    usuarios = relationship('Usuarios', back_populates='permissao', cascade="all, delete-orphan")
