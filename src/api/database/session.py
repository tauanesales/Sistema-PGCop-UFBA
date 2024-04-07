from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.api.config import Config

engine = create_engine(URL(
    drivername=Config.DB_CONFIG.DB_DRIVERNAME,
    username=Config.DB_CONFIG.DB_USERNAME,
    password=Config.DB_CONFIG.DB_PASSWORD,
    host=Config.DB_CONFIG.DB_HOST,
    port=Config.DB_CONFIG.DB_PORT,
    database=Config.DB_CONFIG.DB_DATABASE,
    query={"charset": "utf8"},
))


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
