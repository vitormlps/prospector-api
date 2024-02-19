#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List

# ### Third-party deps
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# ### Local deps
from ..security.current_user_auth import get_current_user
from ..database.connection import get_db_local_session
from ..entities.users.model import Users
from ..entities.cnaes.repository import cnaes_repo, CNAEsView, CNAEsCreate, CNAEsUpdate
from ..entities.base.schema import DefaultQueryFilter


router = APIRouter(tags=["CNAE", "CNAEs"], prefix="/cnaes")


@router.get("", response_model=List[CNAEsView])
def get_all(
        query: DefaultQueryFilter,
        db: Session = Depends(get_db_local_session),
        current_user: Users = Depends(get_current_user),
    ):
    return cnaes_repo.get_all_by(db=db, filters=query)


@router.get("/{id}", response_model=CNAEsView)
def get(
    id: int, 
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return cnaes_repo.get(db=db, id=id)


@router.post("", response_model=CNAEsView)
def create(
    payload: CNAEsCreate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return cnaes_repo.create(db=db, obj_in=payload)


@router.put("/{id}", response_model=CNAEsView)
def update(
    id: int,
    payload: CNAEsUpdate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return cnaes_repo.update(db=db, id=id, obj_in=payload)


@router.delete("/{id}", response_model=CNAEsView)
def delete(
    id: int,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return cnaes_repo.remove(db=db, id=id)
