#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from datetime import datetime

# ### Third-party deps
from sqlalchemy import String, ForeignKey
                                                                # https://docs.sqlalchemy.org/en/20/orm/large_collections.html
from sqlalchemy.orm import relationship, Mapped, mapped_column, WriteOnlyMapped
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base
from ..contatos.model import Contato


class Estabelecimento(Base):
    cnpj_ordem: Mapped[str] = mapped_column(String(4), nullable=False)
    cnpj_digit_verif: Mapped[str] = mapped_column(String(2), nullable=False)
    nome_fantasia: Mapped[str] = mapped_column(nullable=True)
    data_situacao_cadastral: Mapped[datetime] = mapped_column(nullable=False)
    nome_cidade_exterior: Mapped[str] = mapped_column(nullable=True)
    data_inicio_atividade: Mapped[datetime] = mapped_column(nullable=False)
    cnaes_secundarios: Mapped[str] = mapped_column(nullable=True)
    situacao_especial: Mapped[str] = mapped_column(nullable=True)
    data_situacao_especial: Mapped[datetime] = mapped_column(nullable=True)

    empresa_cnpj: Mapped[str] = mapped_column(ForeignKey("empresa.cnpj_basico"), nullable=False, index=True)
    # empresa = relationship("Empresa", back_populates="estabelecimentos", lazy="subquery")

    matriz_filial_id: Mapped[UUID] = mapped_column(ForeignKey("matriz_filial.id"), nullable=False)
    # matriz_filial = relationship("MatrizFilial", back_populates="estabelecimentos", lazy="subquery")

    situacao_cadastral_id: Mapped[UUID] = mapped_column(ForeignKey("situacao_cadastral.id"), nullable=False)
    # situacao_cadastral = relationship("SituacaoCadastral", back_populates="estabelecimentos", lazy="subquery")

    motivo_id: Mapped[UUID] = mapped_column(ForeignKey("motivo.id"), nullable=False)
    # motivo = relationship("Motivo", back_populates="estabelecimentos", lazy="subquery")

    pais_id: Mapped[UUID] = mapped_column(ForeignKey("pais.id"), nullable=True)
    # pais = relationship("Pais", back_populates="estabelecimentos", lazy="subquery")

    cnae_principal_id: Mapped[UUID] = mapped_column(ForeignKey("cnae.id"), nullable=False)
    # cnae_principal = relationship("CNAE", back_populates="estabelecimentos", lazy="subquery")

    logradouro_id: Mapped[UUID] = mapped_column(ForeignKey("logradouro.id"), nullable=False)
    # logradouro = relationship("Logradouro", back_populates="estabelecimentos", lazy="subquery")
    
    # contatos = relationship("Contato", back_populates="estabelecimento", lazy="subquery")
    contatos: WriteOnlyMapped["Contato"] = relationship("Contato", lazy="subquery")
