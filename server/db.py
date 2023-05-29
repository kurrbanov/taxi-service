import redis
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from server import config


engine = create_async_engine(url=config.DB_URL, echo=True)
auth_redis = redis.Redis(host=config.REDIS_HOST, port=6379, db=config.AUTH_DB)

AsyncSessionLocal = async_sessionmaker(autoflush=False, bind=engine)


def get_session() -> AsyncSession:
    return AsyncSessionLocal()


class CustomerBase(DeclarativeBase):
    pass
