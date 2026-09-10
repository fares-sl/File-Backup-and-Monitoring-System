from sqlalchemy import ForeignKey, String, Integer, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from database.engine import Base

class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=False
    )

    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.device_id"),
        primary_key=True
    )

    user: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    path: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    action: Mapped[str] = mapped_column(
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

    __table_args__ = (
        ForeignKeyConstraint(
            ["device_id", "user"],
            ["users.device_id", "users.user"]
        ),
    )