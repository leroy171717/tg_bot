from sqlalchemy import BigInteger, String, ForeignKey, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect, text

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


class DayWeek(Base):
    __tablename__ = 'days'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


class ItemDay(Base):
    __tablename__ = 'items_days'

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))
    day_id: Mapped[int] = mapped_column(ForeignKey('days.id'))


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    price: Mapped[int] = mapped_column()
    category: Mapped['Category'] = mapped_column(ForeignKey('categories.id'))
    image: Mapped[str] = mapped_column(String(50), nullable=True)  # New column


async def add_new_column(engine, table_name, column_name, column_type):
    async with engine.connect() as conn:
        # Use run_sync to perform synchronous operations
        await conn.run_sync(_add_column_if_not_exists, table_name, column_name, column_type)


def _add_column_if_not_exists(conn, table_name, column_name, column_type):
    inspector = inspect(conn)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    if column_name not in columns:
        conn.execute(text(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}'))
        print(f"Column '{column_name}' added to table '{table_name}'")
    else:
        print(f"Column '{column_name}' already exists in table '{table_name}'")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    import asyncio
    asyncio.run(async_main())
