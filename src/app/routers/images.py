#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List

# ### Third-party deps
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# ### Local deps
from ..security.current_user_auth import get_current_user
from ..database.connection import get_db_local_session
from ..entities.users.model import Users
from ..entities.images.repository import images
from ..entities.images.schema import ImagesView, ImagesUpdate, ImageQuery


router = APIRouter(tags=["Image", "Images"], prefix="/images")


@router.get("", response_model=List[ImagesView])
def get_all(
        query: ImageQuery,
        db: Session = Depends(get_db_local_session),
        current_user: Users = Depends(get_current_user),
    ):
    return URLFieldSetter.set_for_images(
        token=current_user["access_token"],
        images=images.get_all_by(db, filters, filters_join, order_by=query.order_by)
    )


@router.get("/{id}", response_model=ImagesView)
def get(
    id: int,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user),
    ):
    img = images.get(db=db, id=id)
    img = URLFieldSetter.set_for_images(token=current_user["access_token"], images=img)[
        0
    ]
    return img


@router.put("/{id}", response_model=ImagesView)
def update(
    id: int,
    payload: ImagesUpdate,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user),
    ):
    return images.update(db=db, id=id, obj_in=payload)


@router.delete("/{id}", response_model=ImagesView)
def delete(
    id: int,
    db: Session = Depends(get_db_local_session),
    current_user: Users = Depends(get_current_user),
    ):
    db_image = images.get(db=db, id=id)

    response = RequestHandler(
        current_user["access_token"]
    ).delete_image(
        inspection_id=db_image.inspection_id,
        equipment_id=db_image.inspection_equipment.equipment_id,
        image_type=db_image.source_type,
        filenames=[db_image.name],
    )

    if 200 >= response.status_code < 300:
        return images.remove(db=db, id=id)
    
    raise HTTPException(response.status_code, response.text)
