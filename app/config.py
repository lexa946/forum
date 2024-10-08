from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT:str
    DATABASE_URL: str

    S3_ENDPOINT_URL:str
    S3_ACCESS_KEY:str
    S3_SECRET_KEY:str
    S3_BUCKET_NAME:str
    S3_TEST_BUCKET_NAME:str

    MODE: Literal["DEV", "TEST", "PROD"]


    @model_validator(mode="before")
    def get_database_url(cls, values):
        values["DATABASE_URL"] = (f"postgresql+asyncpg://{values['DB_USERNAME']}:{values['DB_PASSWORD']}"
                                  f"@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}")
        return values

    DB_TEST_USERNAME: str
    DB_TEST_PASSWORD: str
    DB_TEST_NAME: str
    DB_TEST_HOST: str
    DB_TEST_PORT:str
    DATABASE_TEST_URL: str


    @model_validator(mode="before")
    def get_database_test_url(cls, values):
        values["DATABASE_TEST_URL"] = (f"postgresql+asyncpg://{values['DB_TEST_USERNAME']}:{values['DB_TEST_PASSWORD']}"
                                  f"@{values['DB_TEST_HOST']}:{values['DB_TEST_PORT']}/{values['DB_TEST_NAME']}")
        return values


    class Config:
        env_file = '.env'


settings = Settings()
