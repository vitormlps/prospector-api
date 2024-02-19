#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List

# ### Third-party deps
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# ### Local deps
from ...security.current_user_auth import get_current_user
from ...database.connection import get_db_local_session
from ...entities.users.model import Users
from ...entities.annotations.repository import annotations
from ...entities.annotations.schema import AnnotationsView, AnnotationsCreate, AnnotationsUpdate
from ...entities.base.schema import DefaultQueryFilter


router = APIRouter(tags=["Annotation", "Annotations"], prefix="/annotations")


@router.get("", response_model=List[AnnotationsView])
def get_all(
        query: DefaultQueryFilter,
        db: Session = Depends(get_db_local_session),
        current_user: Users = Depends(get_current_user),
    ):
    return annotations.get_all_by(db=db, filters=query)


@router.get("/{id}", response_model=AnnotationsView)
def get(
    id: int, 
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return annotations.get(db=db, id=id)


@router.post("", response_model=AnnotationsView)
def create(
    payload: AnnotationsCreate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return annotations.create(db=db, obj_in=payload)


@router.put("/{id}", response_model=AnnotationsView)
def update(
    id: int,
    payload: AnnotationsUpdate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return annotations.update(db=db, id=id, obj_in=payload)


@router.delete("/{id}", response_model=AnnotationsView)
def delete(
    id: int,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return annotations.remove(db=db, id=id)
