#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import NaturezasJuridicas
from .schema import NaturezasJuridicasView, NaturezasJuridicasCreate, NaturezasJuridicasUpdate


class NaturezasJuridicasRepo(BaseRepo[NaturezasJuridicas, NaturezasJuridicasCreate, NaturezasJuridicasUpdate]):
    pass


def naturezas_juridicas_repo():
    return NaturezasJuridicasRepo(NaturezasJuridicas)
