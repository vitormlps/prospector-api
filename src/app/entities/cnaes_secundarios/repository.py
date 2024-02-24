#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import CNAEsSecundarios
from .schema import CNAEsSecundariosView, CNAEsSecundariosCreate, CNAEsSecundariosUpdate


class CNAEsSecundariosRepo(BaseRepo[CNAEsSecundarios, CNAEsSecundariosCreate, CNAEsSecundariosUpdate]):
    pass


def cnaes_secundarios_repo():
    return CNAEsSecundariosRepo(CNAEsSecundarios)
