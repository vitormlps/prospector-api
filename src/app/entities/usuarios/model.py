#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base


class Usuarios(Base):
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    permissoes_id = Column(UUID(as_uuid=True), ForeignKey("permissoes.id"), nullable=False)
    permissoes = relationship("Permissoes", back_populates="usuarios", lazy="subquery")
