from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from database.engine import Base

class Agent(Base):
    __tablename__ = 'agent'
    agent_id : Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    hostname : Mapped[str] = mapped_column(String, nullable = False)
    watched_roots : Mapped[list[str]] = mapped_column(ARRAY(String), nullable = False)
    watched_extensions : Mapped[list[str]] = mapped_column(ARRAY(String), nullable = False)
    period : Mapped[int] = mapped_column(Integer, nullable = False)
    last_resolved_action_id : Mapped[int] = mapped_column(Integer, default = 0, nullable = False)

    