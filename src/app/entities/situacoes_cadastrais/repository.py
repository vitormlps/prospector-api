#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import SituacaoCadastral
from .schema import SituacoesCadastraisView, SituacoesCadastraisCreate, SituacoesCadastraisUpdate


class SituacoesCadastraisRepo(BaseRepo[SituacaoCadastral, SituacoesCadastraisCreate, SituacoesCadastraisUpdate]):
    pass


def situacoes_cadastrais_repo():
    return SituacoesCadastraisRepo(SituacaoCadastral)
