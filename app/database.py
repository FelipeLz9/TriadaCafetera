from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

# Importar modelos después de definir Base para evitar importación circular
# Los modelos se importarán cuando se necesiten

async def get_db():
    async with SessionLocal() as session:
        yield session
        
async def create_tables():
    # Los modelos deben importarse antes de llamar a esta función
    # Se importan en main.py para evitar importación circular
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 