#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Qualificacoes
from .schema import QualificacoesView, QualificacoesCreate, QualificacoesUpdate


class QualificacoesRepo(BaseRepo[Qualificacoes, QualificacoesCreate, QualificacoesUpdate]):
    pass


def qualificacoes_repo():
    return QualificacoesRepo(Qualificacoes)
