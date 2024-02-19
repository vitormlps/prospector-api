#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Estabelecimentos
from .schema import EstabelecimentosView, EstabelecimentosCreate, EstabelecimentosUpdate


class EstabelecimentosRepo(BaseRepo[Estabelecimentos, EstabelecimentosCreate, EstabelecimentosUpdate]):
    pass


def estabelecimentos_repo():
    return EstabelecimentosRepo(Estabelecimentos)
