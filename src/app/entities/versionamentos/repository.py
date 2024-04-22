#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Versionamento
from .schema import VersionamentosView, VersionamentosCreate, VersionamentosUpdate


class VersionamentosRepo(BaseRepo[Versionamento, VersionamentosCreate, VersionamentosUpdate]):
    pass


def versionamentos_repo():
    return VersionamentosRepo(Versionamento)
