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
from ..entities.roles.repository import roles
from ..entities.roles.schema import RolesCreate, RolesUpdate, RolesView
from ..entities.base.schema import DefaultQueryFilter


router = APIRouter(tags=["Role", "Roles"], prefix='/users/roles')


@router.get("", response_model=List[RolesView])
def get_all(
        query: DefaultQueryFilter,
        db: Session = Depends(get_db_local_session),
        current_user: Users = Depends(get_current_user),
    ):
    return roles.get_all_by(db=db, filters=query)


@router.get("/{id}", response_model=RolesView)
def get(
    id: int, 
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return roles.get(db=db, id=id)



@router.post("", response_model=RolesView)
def create(
    payload: RolesCreate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return roles.create(db=db, obj_in=payload)


@router.put("/{id}", response_model=RolesView)
def update(
    id: int,
    payload: RolesUpdate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return roles.update(db=db, id=id, obj_in=payload)


@router.delete("/{id}", response_model=RolesView)
def delete(
    id: int,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return roles.remove(db=db, id=id)
