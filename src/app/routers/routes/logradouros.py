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
from ...entities.logradouros.repository import logradouros_repo, LogradourosView, LogradourosCreate, LogradourosUpdate, LogradourosFilter


router = APIRouter(tags=["Logradouros"], prefix="/logradouros")


@router.get("", response_model=List[LogradourosView])
def get_all_by(
        query: LogradourosFilter = Depends(LogradourosFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = logradouros_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Logradouros not found")

    return result


@router.get("/{id}", response_model=LogradourosView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = logradouros_repo().get(id)

    if result is None:
        raise HTTPException(404, "Logradouro not found")

    return result


@router.post("", response_model=LogradourosView)
def create(
        payload: LogradourosCreate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = logradouros_repo().create(payload)

    if result is None:
        raise HTTPException(500, "Logradouro could not be created")

    return result


@router.put("/{id}", response_model=LogradourosView)
def update(
        id: UUID,
        payload: LogradourosUpdate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = logradouros_repo().update(id=id, obj_in=payload)

    if result is None:
        raise HTTPException(500, "Logradouro could not be updated")

    return result


@router.delete("/{id}", response_model=LogradourosView)
def delete(
        id: UUID,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = logradouros_repo().remove(id)
    
    if not result:
        raise HTTPException(500, "Logradouro could not be deleted")
    
    return Response(200, "Logradouro successfully deleted")