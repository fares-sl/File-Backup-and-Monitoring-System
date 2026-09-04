from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database.engine import Base

class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(
        Integer,
        autoincrement=False,
        primary_key=True
    )

    agent_id: Mapped[int] = mapped_column(
        ForeignKey("agent.agent_id"),
        primary_key=True
    )

    path: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    action: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    user: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    action_time: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    old_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )