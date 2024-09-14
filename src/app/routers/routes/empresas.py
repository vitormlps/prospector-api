#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List
from uuid import UUID
from io import BytesIO

# ### Third-party deps
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse

# ### Local deps
from ...security.current_user_auth import get_current_user
from ...entities.usuarios.model import Usuario
from ...entities.empresas.repository import empresas_repo, EmpresasView, EmpresasCreate, EmpresasUpdate, EmpresasFilter, EmpresasMainView


router = APIRouter(tags=["Empresas"], prefix="/empresas")


@router.get("", response_model=List[EmpresasMainView])
def get_all_by(
        query: EmpresasFilter = Depends(EmpresasFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = empresas_repo().get_all_by(filters=query)

    if len(result) == 0:
        raise HTTPException(404, "Empresas not found")

    return result


@router.get("/{id}", response_model=EmpresasView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = empresas_repo().get(id)

    if result is None:
        raise HTTPException(404, "Empresa not found")

    return result


@router.post("", response_model=EmpresasView)
def create(
        payload: EmpresasCreate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = empresas_repo().create(payload)

    if result is None:
        raise HTTPException(500, "Empresa could not be created")

    return result


@router.put("/{id}", response_model=EmpresasView)
def update(
        id: UUID,
        payload: EmpresasUpdate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = empresas_repo().update(id=id, obj_in=payload)

    if result is None:
        raise HTTPException(500, "Empresa could not be updated")

    return result


@router.delete("/{id}", response_model=EmpresasView)
def delete(
        id: UUID,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = empresas_repo().remove(id)
    
    if not result:
        raise HTTPException(500, "Empresa could not be deleted")
    
    return Response(200, "Empresa successfully deleted")


@router.post("/export", response_class=StreamingResponse)
def generate_csv(
        payload: List[UUID],
        current_user: Usuario = Depends(get_current_user)
    ):
    result = empresas_repo().generate_csv(payload)

    if result is None:
        raise HTTPException(404, "Empresas not found")

    return StreamingResponse(
        result,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )