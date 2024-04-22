#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy.orm import relationship, Mapped, mapped_column, WriteOnlyMapped


# ### Local deps
from ..base.model import Base
from ..empresas.model import Empresa
from ..socios.model import Socio
from ..representantes_legais.model import RepresentanteLegal


class Qualificacao(Base):
    codigo: Mapped[str] = mapped_column(nullable=False, unique=True)
    descricao: Mapped[str] = mapped_column(nullable=False)

    # empresas = relationship("Empresa", back_populates="qualificacao_responsavel", lazy="subquery")
    empresas: WriteOnlyMapped["Empresa"] = relationship("Empresa", lazy="subquery")

    # socios = relationship("Socio", back_populates="qualificacao", lazy="subquery")
    socios: WriteOnlyMapped["Socio"] = relationship("Socio", lazy="subquery")

    # representantes_legais = relationship("RepresentanteLegal", back_populates="qualificacao", lazy="subquery")
    representantes_legais: WriteOnlyMapped["RepresentanteLegal"] = relationship("RepresentanteLegal", lazy="subquery")
