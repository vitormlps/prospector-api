#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Dict, Generic, List, Optional, Type, TypeVar
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel
from sqlalchemy import or_, and_, text, select, insert, update, delete, Delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

# ### Local deps
from app.helpers import Logger
from app.database.connection import get_db_local_session, get_db_engine
from .model import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepo(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._logger = Logger().get_logger()

        self.session: Session = next(get_db_local_session())
        self.model = model


    def get_index_sequence(self):
        db_data = self.session.execute(text("SELECT nextval(:index_seq);"), index_seq=self.__INDEX_SEQUENCE)
        data = [dict(data) for data in db_data]
        return data[0]["nextval"]


    def __qualify_filters(self, filters, skip, limit):

        if isinstance(filters, BaseModel):
            skip, limit = filters.skip, filters.limit
            filters = filters.dict(exclude_none=True, exclude={'skip', 'limit'})
        
        else:
            skip, limit = filters.pop("skip"), filters.pop("limit")
            temp_filters = filters.copy()
            [filters.pop(key) for key, value in temp_filters.items() if value is None]

        return filters, skip, limit


    def get_all_by(self, 
            filters: BaseModel | Dict, 
            order_by: str = "created_at", 
            skip: int = 0, 
            limit: int = 0
        ) -> Optional[List[ModelType]]:

        filters, skip, limit = self.__qualify_filters(filters, skip, limit)

        query = select(self.model).filter_by(**filters).order_by(order_by)

        if skip != 0:
            query = query.offset(skip)
        
        if limit != 0:
            query = query.limit(limit)

        return self.execute_query_all(query)


    def get(self, id: UUID) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)

        return self.execute_query_single(query)


    def get_by(self, filters: BaseModel) -> Optional[ModelType]:
        filters, _, _ = self.__qualify_filters(filters, 0, 0)
        query = select(self.model).filter_by(**filters)

        return self.execute_query_single(query)


    def create(self, payload, commit=True) -> ModelType:
        query = insert(self.model).values(**payload).returning(self.model)

        if commit:
            return self.execute_transaction(query)
        
        return self.execute_query_single(query)


    def update(self, id: UUID, payload, commit=True) -> ModelType:
        query = update(self.model).where(self.model.id == id).values(**payload).returning(self.model)
        
        if commit:
            return self.execute_transaction(query)
        
        return self.execute_query_single(query)


    def remove(self, id: UUID, commit=True) -> Optional[bool]:
        query = delete(self.model).where(self.model.id == id)
        
        if commit:
            return self.execute_transaction(query)
        
        return self.execute_query_single(query)


    def count(self) -> int:
        result = 0

        try:
            result = self.session.execute(
                text(f"SELECT COUNT(id) FROM {self.model.__tablename__};"), 
            ).one()[0]

        except Exception as err:
            self._logger.debug(f"Error while counting: {err}")

        finally:
            return result


    def execute_query_all(self, query):
        results = None

        try:
            results = self.session.execute(query).all()
            results = [result[0] for result in results]

        except NoResultFound:
            self._logger.warning("No result found")

        except Exception as err:
            self._logger.error(f"Error with {self.model}: {err}")
        
        # self.close_session()
        return results


    def execute_query_single(self, query):
        result = None

        try:
            if isinstance(query, Delete):
                self.session.execute(query)
                result = True
            else:
                result = self.session.execute(query).one()[0]
        
        except NoResultFound:
            self._logger.debug("No result found")

        except Exception as err:
            self._logger.debug(f"Error with {self.model}: {err}")

        return result


    def execute_transaction(self, query):
        result = None

        try:
            self.session.begin()

            if isinstance(query, Delete):
                self.session.execute(query)
                result = True
            else:
                result = self.session.execute(query).one()[0]

            self.session.commit()

        except NoResultFound:
            self._logger.debug("No result found")
            self.session.rollback()

        except Exception as err:
            self._logger.debug(f"Error with {self.model}: {err}")
            self.session.rollback()

        return result


    def close_session(self):
        self.session.close()


def create_all():
    Base.metadata.create_all(bind=get_db_engine())


def drop_all():
    Base.metadata.drop_all(bind=get_db_engine())


def reset_db():
    drop_all()
    create_all()
