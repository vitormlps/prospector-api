#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Permissao
from .schema import PermissoesView, PermissoesCreate, PermissoesUpdate


class PermissoesRepo(BaseRepo[Permissao, PermissoesCreate, PermissoesUpdate]):
    pass


def permissoes_repo():
    return PermissoesRepo(Permissao)
