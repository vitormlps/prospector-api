#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Usuario
from .schema import UsuariosView, UsuariosCreate, UsuariosUpdate
from ...utils.encryptors import encrypt_pw


class UsuariosRepo(BaseRepo[Usuario, UsuariosCreate, UsuariosUpdate]):
    def create(self, db, *, obj_in: UsuariosCreate) -> Usuario:
        obj_in.password = encrypt_pw(obj_in.password)
        db_obj = Usuario(**obj_in.dict())
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj


    def update(self, db, *, db_obj: Usuario, obj_in: UsuariosUpdate) -> Usuario:
        obj_in.password = encrypt_pw(obj_in.password)
        
        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)


def usuarios_repo():
    return UsuariosRepo(Usuario)
