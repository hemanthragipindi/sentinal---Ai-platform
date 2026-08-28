from typing import Any, Generic, TypeVar, Sequence
from datetime import datetime, timezone
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.expression import Select

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get_by_id(self, db: AsyncSession, id: Any) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == id, self.model.deleted_at.is_(None))
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_by_id_with_deleted(self, db: AsyncSession, id: Any) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def list(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        stmt = select(self.model).where(self.model.deleted_at.is_(None)).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def count(self, db: AsyncSession, base_stmt: Select | None = None) -> int:
        if base_stmt is None:
            base_stmt = select(self.model).where(self.model.deleted_at.is_(None))
        stmt = select(func.count()).select_from(base_stmt.subquery())
        result = await db.execute(stmt)
        return result.scalar_one()

    async def exists(self, db: AsyncSession, id: Any) -> bool:
        stmt = select(self.model.id).where(self.model.id == id, self.model.deleted_at.is_(None))
        result = await db.execute(stmt)
        return result.scalars().first() is not None

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType | dict[str, Any]) -> ModelType:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)
            
        db_obj = self.model(**create_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def soft_delete(self, db: AsyncSession, id: Any) -> bool:
        stmt = update(self.model).where(self.model.id == id, self.model.deleted_at.is_(None)).values(deleted_at=datetime.now(timezone.utc))
        result = await db.execute(stmt)
        await db.flush()
        return result.rowcount > 0

    async def restore(self, db: AsyncSession, id: Any) -> bool:
        stmt = update(self.model).where(self.model.id == id).values(deleted_at=None)
        result = await db.execute(stmt)
        await db.flush()
        return result.rowcount > 0

    async def delete(self, db: AsyncSession, id: Any) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        await db.flush()
        return result.rowcount > 0
