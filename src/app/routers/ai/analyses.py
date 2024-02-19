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
from ...entities.analyses.repository import analyses
from ...entities.analyses.schema import AnalysesView, AnalysesCreate, AnalysesUpdate
from ...entities.base.schema import DefaultQueryFilter


router = APIRouter(tags=["Analysis", "Analyses"], prefix="/analyses")


@router.get("", response_model=List[AnalysesView])
def get_all(
        query: DefaultQueryFilter,
        db: Session = Depends(get_db_local_session),
        current_user: Users = Depends(get_current_user),
    ):
    return analyses.get_all_by(db=db, filters=query)


@router.get("/{id}", response_model=AnalysesView)
def get(
    id: int, 
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return analyses.get(db=db, id=id)


@router.post("", response_model=AnalysesView)
def create(
    payload: AnalysesCreate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return analyses.create(db=db, obj_in=payload)


@router.put("/{id}", response_model=AnalysesView)
def update(
    id: int,
    payload: AnalysesUpdate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return analyses.update(db=db, id=id, obj_in=payload)


@router.delete("/{id}", response_model=AnalysesView)
def delete(
    id: int,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return analyses.remove(db=db, id=id)
