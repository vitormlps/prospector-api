#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Municipios
from .schema import MunicipiosView, MunicipiosCreate, MunicipiosUpdate


class MunicipiosRepo(BaseRepo[Municipios, MunicipiosCreate, MunicipiosUpdate]):
    pass


def municipios_repo():
    return MunicipiosRepo(Municipios)
