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
from ..entities.users.repository import users
from ..entities.users.schema import UsersView, UsersCreate, UsersUpdate
from ..entities.base.schema import DefaultQueryFilter


router = APIRouter(tags=["User", "Users"], prefix="/users")


@router.get("", response_model=List[UsersView])
def get_all(
        query: DefaultQueryFilter,
        db: Session = Depends(get_db_local_session),
        current_user: Users = Depends(get_current_user),
    ):
    return users.get_all_by(db=db, filters=query)


@router.get("/{id}", response_model=UsersView)
def get(
    id: int, 
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return users.get(db=db, id=id)


@router.post("", response_model=UsersView)
def create(
    payload: UsersCreate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return users.create(db=db, obj_in=payload)


@router.put("/{id}", response_model=UsersView)
def update(
    id: int,
    payload: UsersUpdate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return users.update(db=db, id=id, obj_in=payload)


@router.delete("/{id}", response_model=UsersView)
def delete(
    id: int,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return users.remove(db=db, id=id)
