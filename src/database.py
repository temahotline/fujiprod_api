from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import settings


engine = create_async_engine(
    settings.REAL_DATABASE_URL, future=True, echo=True
)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
