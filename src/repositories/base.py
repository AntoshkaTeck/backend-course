import logging
from typing import TypeVar, Generic, Sequence

from asyncpg import UniqueViolationError, ForeignKeyViolationError
from pydantic import BaseModel
from sqlalchemy import select, delete, update, insert
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.database import Base
from src.exceptions import (
    ObjectNotFoundException,
    ObjectAlreadyExistsException,
    ObjectEmptyFieldsException,
    ObjectLinkNotFoundException,
)
from src.repositories.mappers.base import DataMapper


DBModel = TypeVar("DBModel", bound=Base)
Schema = TypeVar("Schema", bound=BaseModel)


class BaseRepository(Generic[DBModel, Schema]):
    model: type[DBModel]
    mapper: type[DataMapper[DBModel, Schema]]

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *where, **filter_by):
        query = select(self.model).where(*where).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
            return self.mapper.map_to_domain_entity(model)
        except NoResultFound:
            raise ObjectNotFoundException

    async def add(self, data: BaseModel):
        try:
            add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as ex:
            logging.exception(f"Не удалось добавить данные в БД, входные данные: {data=}")
            cause = getattr(ex.orig, "__cause__", None)
            if isinstance(cause, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            logging.exception(
                f"Не знакомая ошибка, не удалось добавить данные в БД, входные данные: {data=}"
            )
            raise ex

    async def add_bulk(self, data: Sequence[BaseModel]):
        try:
            add_stmt = insert(self.model).values([item.model_dump() for item in data])
            await self.session.execute(add_stmt)
        except IntegrityError as ex:
            # ловим конкретно FK violation от asyncpg
            cause = getattr(ex.orig, "__cause__", None)
            if isinstance(cause, ForeignKeyViolationError):
                raise ObjectLinkNotFoundException from ex

    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        values = data.model_dump(exclude_unset=exclude_unset)
        if not values:
            raise ObjectEmptyFieldsException
        update_stmt = update(self.model).filter_by(**filter_by).values(values).returning(self.model)
        result = await self.session.execute(update_stmt)
        model = result.scalar_one()
        return self.mapper.map_to_domain_entity(model)

    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
