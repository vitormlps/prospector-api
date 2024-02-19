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
from ..entities.comments.repository import comments
from ..entities.comments.schema import CommentsView, CommentsCreate, CommentsUpdate
from ..entities.base.schema import DefaultQueryFilter


# puxar com users

router = APIRouter(tags=["Comment", "Comments"], prefix='/analyses')


@router.get("/{analysis_id}/comments", response_model=List[CommentsView])
def get_all(
        analysis_id: int,
        query: DefaultQueryFilter,
        db: Session = Depends(get_db_local_session),
        current_user: Users = Depends(get_current_user),
    ):
    return comments.get_all_by(db=db, filters=query)


@router.get("/comments/{id}", response_model=CommentsView)
def get(
        id: int,
        db: Session = Depends(get_db_local_session),
        current_user: Users = Depends(get_current_user),
    ):
    return comments.get(db=db, id=id)


@router.post("/comments", response_model=CommentsView)
def create(
    payload: CommentsCreate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return comments.create(db=db, obj_in=payload)


@router.put("/comments/{id}", response_model=CommentsView)
def update(
    id: int,
    payload: CommentsUpdate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return comments.update(db=db, id=id, obj_in=payload)


@router.delete("/comments/{id}", response_model=CommentsView)
def delete(
    id: int,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return comments.remove(db=db, id=id)
