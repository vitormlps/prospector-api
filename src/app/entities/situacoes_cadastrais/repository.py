#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import select

# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import SituacaoCadastral
from .schema import SituacoesCadastraisView, SituacoesCadastraisCreate, SituacoesCadastraisUpdate


class SituacoesCadastraisRepo(BaseRepo[SituacaoCadastral, SituacoesCadastraisCreate, SituacoesCadastraisUpdate]):
    def get_all_ids(self):
        query = select(self.model.id, self.model.codigo)
        results = self.session.execute(query).all()
        return results


def situacoes_cadastrais_repo():
    return SituacoesCadastraisRepo(SituacaoCadastral)
