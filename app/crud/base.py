from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models.user import User

ModelType = TypeVar('ModelType', bound=Base)


class CRUDBase(Generic[ModelType, ]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ) -> ModelType:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> List[ModelType]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ) -> ModelType:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_project: ModelType,
            update_obj,
            session: AsyncSession
    ) -> ModelType:
        obj_data = jsonable_encoder(db_project)
        update_data = update_obj.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_project, field, update_data[field])

        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
        return db_project

    async def remove(
            self,
            db_obj: ModelType,
            session: AsyncSession
    ) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
