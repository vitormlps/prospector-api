#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Socio
from .schema import SociosView, SociosCreate, SociosUpdate, SociosFilter


class SociosRepo(BaseRepo[Socio, SociosCreate, SociosUpdate]):
    pass


def socios_repo():
    return SociosRepo(Socio)
