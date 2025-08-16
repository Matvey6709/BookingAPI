from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app import config

# alembic downgrade - 1
# alembic revision --autogenerate -m 'initial migration'
# alembic upgrade head

DATA_BASE_URL = config.s.DATA_BASE_URL
DATA_BASE_PARAMS = {}

if config.s.MODE == 'TEST':
    DATA_BASE_URL = config.s.TEST_DATA_BASE_URL
    DATA_BASE_PARAMS = {'poolclass': NullPool}

engine = create_async_engine(DATA_BASE_URL, **DATA_BASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
