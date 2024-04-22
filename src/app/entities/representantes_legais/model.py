#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, WriteOnlyMapped
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base
from ..socios.model import Socio


class RepresentanteLegal(Base):
    cpf: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    nome: Mapped[str] = mapped_column(nullable=False)

    qualificacao_id: Mapped[UUID] = mapped_column(ForeignKey("qualificacao.id"), nullable=False)
    # qualificacao = relationship("Qualificacao", back_populates="representantes_legais", lazy="subquery")

    # socios = relationship("Socio", back_populates="representante_legal", lazy="subquery")
    socios: WriteOnlyMapped["Socio"] = relationship("Socio", lazy="subquery")
