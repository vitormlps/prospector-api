#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import SimplesNacional
from .schema import SimplesNacionalView, SimplesNacionalCreate, SimplesNacionalUpdate


class SimplesNacionalRepo(BaseRepo[SimplesNacional, SimplesNacionalCreate, SimplesNacionalUpdate]):
    pass


def simples_nacional_repo():
    return SimplesNacionalRepo(SimplesNacional)
