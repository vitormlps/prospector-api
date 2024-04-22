#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base


class Contato(Base):
    tipo: Mapped[str] = mapped_column(nullable=False)
    descricao: Mapped[str] = mapped_column(nullable=False)

    estabelecimento_id: Mapped[UUID] = mapped_column(ForeignKey("estabelecimento.id"), nullable=False, index=True)
    # estabelecimento = relationship("Estabelecimento", back_populates="contatos", lazy='subquery')
