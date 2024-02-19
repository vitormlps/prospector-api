from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from app.entities.base.model import Base
from .filters import Filter, FilterJoin, FilterDateBetween


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all_by_join(
        self,
        db: Session,
        filters: List[Filter] = None,
        filters_join: List[FilterJoin] = None,
        filter_date: FilterDateBetween = None,
        order_by=None,
    ):
        query_filters = []

        if filters is not None:
            for filter in filters:
                filter_conditions = [
                    getattr(self.model, filter.key) == value for value in filter.values
                ]
                query_filters.append(or_(*filter_conditions))
        query_filters = and_(*query_filters)

        query = db.query(self.model)

        if filters_join is not None:
            for filter in filters_join:
                query = query.join(filter.class_, filter.class_attr == filter.join_attr)
                filter_conditions = (
                    [
                        getattr(filter.class_, filter.class_key) == value
                        for value in filter.values
                    ]
                    if filter.values
                    else []
                )
                query_filters = and_(query_filters, or_(*filter_conditions))

        query = query.filter(query_filters)

        if filter_date is not None:
            query = query.filter(
                filter_date.key.between(filter_date.start, filter_date.end)
            )

        return query.order_by(order_by).all()


    def get_by_and(self, db: Session, filters: dict) -> Optional[ModelType]:
        filter = []
        for k, v in filters.items():
            if isinstance(v, tuple):
                filter.append(getattr(self.model, k).in_(v))
            else:
                filter.append(getattr(self.model, k) == v)
        
        return db.query(self.model).filter(*filter).first()


    def get_all_by(self, db: Session, filters: BaseModel | Dict, skip: int = 0, limit: int = 100) -> Optional[List[ModelType]]:
        if isinstance(filters, BaseModel):
            skip, limit = filters.skip, filters.limit
            filters = filters.dict(exclude_none=True, exclude={'skip', 'limit'})
        return db.query(self.model).filter_by(**filters).order_by(self.model.id).offset(skip).limit(limit).all()
    

    def get_by(self, db: Session, filters: dict) -> Optional[ModelType]:
        return db.query(self.model).filter_by(**filters)


    def get_all(self, db: Session, *, skip: int = 0, limit: int = 100, no_limit: bool = False) -> Optional[List[ModelType]]:
        query = db.query(self.model).order_by(self.model.id)
        if not no_limit:
            query = query.offset(skip).limit(limit)
        return query.all()


    def get(self, db: Session, id: Union[int, str]) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_or_404(self, db: Session, id: Union[int, str]) -> Optional[ModelType]:
        db_query = db.query(self.model).filter(self.model.id == id).first()
        if not db_query:
            raise HTTPException(404, f"{self.model.__name__} not found")
        return db_query

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)

        try:
            db.add(db_obj)
        except HTTPException as err:
            raise err
        except Exception as err:
            raise HTTPException(500, str(err))

        db.commit()
        db.refresh(db_obj)
        return db_obj


    def create_with_association(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def update(self, db: Session, *, id: Union[int, str], 
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        db_obj = self.get(db, id)
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def remove(self, db: Session, *, id: Union[int, str]) -> ModelType:
        db_obj = self.get(db, id)
        db.delete(db_obj)
        db.commit()
        return db_obj
