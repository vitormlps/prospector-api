#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Estabelecimento
from .schema import EstabelecimentosView, EstabelecimentosCreate, EstabelecimentosUpdate, EstabelecimentosFilter


class EstabelecimentosRepo(BaseRepo[Estabelecimento, EstabelecimentosCreate, EstabelecimentosUpdate]):
    pass


def estabelecimentos_repo():
    return EstabelecimentosRepo(Estabelecimento)
