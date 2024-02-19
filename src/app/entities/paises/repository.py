#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Paises
from .schema import PaisesView, PaisesCreate, PaisesUpdate


class PaisesRepo(BaseRepo[Paises, PaisesCreate, PaisesUpdate]):
    pass


def paises_repo():
    return PaisesRepo(Paises)
