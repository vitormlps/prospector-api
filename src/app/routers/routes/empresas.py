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
from ...entities.empresas.repository import empresas_repo, EmpresasView, EmpresasCreate, EmpresasUpdate, EmpresasFilter


router = APIRouter(tags=["Empresas"], prefix="/empresas")


@router.get("", response_model=List[EmpresasView])
def get_all_by(
        query: EmpresasFilter = Depends(EmpresasFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    # print(query)
    # nat_jurs = query.natureza_juridica_id.split(",") if query.natureza_juridica_id else None
    # portes = query.porte_empresa_id.split(",") if query.porte_empresa_id else None
    # situ_cads = query.situacao_cadastral_id.split(",") if query.situacao_cadastral_id else None
    # cnaes = query.cnae_id.split(",") if query.cnae_id else None

    # query = query.dict()
    # query["natureza_juridica_id"] = nat_jurs
    # query["porte_empresa_id"] = portes
    # query["situacao_cadastral_id"] = situ_cads
    # query["cnae_id"] = cnaes
    
    # result = empresas_repo().filter_by(filters=query)
    result = empresas_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
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