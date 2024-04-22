#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy.orm import relationship, Mapped, mapped_column, WriteOnlyMapped

# ### Local deps
from ..base.model import Base
from ..estabelecimentos.model import Estabelecimento


class SituacaoCadastral(Base):
    codigo: Mapped[str] = mapped_column(nullable=False, unique=True)
    descricao: Mapped[str] = mapped_column(nullable=False)

    # estabelecimentos = relationship("Estabelecimento", back_populates="situacao_cadastral", lazy="subquery")
    estabelecimentos: WriteOnlyMapped["Estabelecimento"] = relationship("Estabelecimento", lazy="subquery")
