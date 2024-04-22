#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Logradouro
from .schema import LogradourosView, LogradourosCreate, LogradourosUpdate, LogradourosFilter


class LogradourosRepo(BaseRepo[Logradouro, LogradourosCreate, LogradourosUpdate]):
    pass


def logradouros_repo():
    return LogradourosRepo(Logradouro)
