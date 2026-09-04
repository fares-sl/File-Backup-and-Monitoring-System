from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import config


class Base(DeclarativeBase):
    pass

from database.models.actions import Action
from database.models.Agent import Agent

engine = create_engine(config.DB_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind = engine, autoflush = False, autocommit = False)