import os
from typing import Literal

from dotenv import load_dotenv


class Settings:
    load_dotenv()

    MODE: Literal['DEV', 'TEST', 'PROD'] = os.getenv('MODE')
    LOG_LEVEL: Literal['INFO', 'DEBUG'] = os.getenv('LOG_LEVEL')

    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = int(os.getenv('DB_PORT'))
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_NAME = os.getenv('DB_NAME')
    DATA_BASE_URL = fr'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    TEST_DB_HOST = os.getenv('TEST_DB_HOST')
    TEST_DB_PORT = int(os.getenv('TEST_DB_PORT'))
    TEST_DB_USER = os.getenv('TEST_DB_USER')
    TEST_DB_PASS = os.getenv('TEST_DB_PASS')
    TEST_DB_NAME = os.getenv('TEST_DB_NAME')
    TEST_DATA_BASE_URL = fr'postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}'

    Secret_JWT_KEY = os.getenv('Secret_JWT_KEY')
    ALGORITM = os.getenv('ALGORITM')
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')


s = Settings()
Secret_JWT_KEY = s.Secret_JWT_KEY
ALGORITM = s.ALGORITM
