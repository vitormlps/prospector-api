#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List
from uuid import UUID

# ### Third-party deps
from fastapi import APIRouter, Depends, HTTPException, Response

# ### Local deps
from ...security.current_user_auth import get_current_user
from ...entities.usuarios.model import Usuario
from ...entities.cnaes.repository import cnaes_repo, CNAEsView, CNAEsCreate, CNAEsUpdate
from ...entities.base.schema import BaseFilter


router = APIRouter(tags=["CNAEs"], prefix="/cnaes")


@router.get("", response_model=List[CNAEsView])
def get_all_by(
        query: BaseFilter = Depends(BaseFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = cnaes_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "CNAEs not found")

    return result


@router.get("/{id}", response_model=CNAEsView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = cnaes_repo().get(id)

    if result is None:
        raise HTTPException(404, "CNAE not found")

    return result


@router.post("", response_model=CNAEsView)
def create(
        payload: CNAEsCreate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = cnaes_repo().create(payload)

    if result is None:
        raise HTTPException(500, "CNAE could not be created")

    return result


@router.put("/{id}", response_model=CNAEsView)
def update(
        id: UUID,
        payload: CNAEsUpdate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = cnaes_repo().update(id=id, obj_in=payload)

    if result is None:
        raise HTTPException(500, "CNAE could not be updated")

    return result


@router.delete("/{id}", response_model=CNAEsView)
def delete(
        id: UUID,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = cnaes_repo().remove(id)
    
    if not result:
        raise HTTPException(500, "CNAE could not be deleted")
    
    return Response(200, "CNAE successfully deleted")