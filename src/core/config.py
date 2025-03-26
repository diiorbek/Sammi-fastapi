from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    MODE: str

    SECRET_KEY: str
    REFRESH_SECRET_KEY : str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ALGORITHM: str


class PgSettings(BaseSettings):
    POSTGRES_DRV: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    @property
    def connection_string(self) -> str:
        return (
            f'{self.POSTGRES_DRV}://'
            f'{self.POSTGRES_USER}:'
            f'{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/'
            f'{self.POSTGRES_DB}'
        )


app_settings = AppSettings()
pg_settings = PgSettings()
