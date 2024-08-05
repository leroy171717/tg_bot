from database.models import async_session
from database.models import User, Category, Item, ItemDay, DayWeek
from sqlalchemy import select, and_


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def get_days():
    async with async_session() as session:
        return await session.scalars(select(DayWeek))

async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))

async def get_category_item(category_id, day_id):
    async with async_session() as session:
        query = (
            select(Item)
            .join(ItemDay, Item.id == ItemDay.item_id)
            .join(DayWeek, ItemDay.day_id == DayWeek.id)
            .where(and_(DayWeek.id == day_id, Item.category == category_id))
        )
        return await session.scalars(query)


async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))