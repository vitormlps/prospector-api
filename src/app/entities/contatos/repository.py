#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Contato
from .schema import ContatosView, ContatosCreate, ContatosUpdate, ContatosFilter


class ContatosRepo(BaseRepo[Contato, ContatosCreate, ContatosUpdate]):
    pass


def contatos_repo():
    return ContatosRepo(Contato)
