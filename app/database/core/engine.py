from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings


async_engine = create_async_engine(url=settings.database_url_asyncpg)

async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass
