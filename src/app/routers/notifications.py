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
from ..entities.notifications.repository import notifications
from ..entities.notifications.schema import NotificationsCreate, NotificationsUpdate, NotificationsView
from ..entities.base.schema import DefaultQueryFilter


router = APIRouter(tags=["Notification", "Notifications"], prefix="/notifications")


@router.get("", response_model=List[NotificationsView])
def get_all(
    query: DefaultQueryFilter,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return notifications.get_all(db=db)


@router.get("/{id}", response_model=NotificationsView)
def get(
    id: int, 
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user)
    ):
    return notifications.get(db=db, id=id)


@router.post("", response_model=NotificationsView)
def create(
    payload: NotificationsCreate,
    db: Session = Depends(get_db_local_session), 
    current_user: Users = Depends(get_current_user),
    ):
    return notifications.create(db=db, obj_in=payload)


@router.put("/{id}", response_model=NotificationsView)
def update(
    id: int,
    payload: NotificationsUpdate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user),
    ):
    return notifications.update(db=db, id=id, obj_in=payload)


@router.delete("/{id}", response_model=NotificationsView)
def delete(
    id: int,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user),
    ):
    return notifications.remove(db=db, id=id)
