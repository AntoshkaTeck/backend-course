import logging

from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import select, delete, update, insert
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

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
            logging.exception(
                f"Не удалось добавить данные в БД, входные данные: {data=}"
            )
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                logging.exception(
                    f"Не знакомая ошибка, не удалось добавить данные в БД, входные данные: {data=}"
                )
                raise ex

    async def add_bulk(self, data: list[BaseModel]):
        add_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_stmt)

    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(update_stmt)
        model = result.scalar_one()
        return self.mapper.map_to_domain_entity(model)

    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
