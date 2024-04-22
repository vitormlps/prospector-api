#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import select

# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Qualificacao
from .schema import QualificacoesView, QualificacoesCreate, QualificacoesUpdate


class QualificacoesRepo(BaseRepo[Qualificacao, QualificacoesCreate, QualificacoesUpdate]):
    def get_all_ids(self):
        query = select(self.model.id, self.model.codigo)
        results = self.session.execute(query).all()
        return results


def qualificacoes_repo():
    return QualificacoesRepo(Qualificacao)
