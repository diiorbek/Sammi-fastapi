from sqlalchemy.ext.asyncio import AsyncSession , create_async_engine, async_sessionmaker
from core.config import pg_settings

engine = create_async_engine(pg_settings.connection_string, echo = True)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit = False,
)

async def get_db():
    async with SessionLocal() as a_session:
        try:
            yield a_session
        except:
            await a_session.rollback()
