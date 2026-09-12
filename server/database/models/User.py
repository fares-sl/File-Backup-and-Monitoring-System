from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from database.engine import Base

class User(Base):
    __tablename__ = 'users'
    device_id : Mapped[int] = mapped_column(Integer, ForeignKey('devices.device_id'), primary_key = True)
    user : Mapped[str] = mapped_column(String, primary_key = True)
    watched_roots : Mapped[list[str]] = mapped_column(ARRAY(String), nullable = False)
    watched_extensions : Mapped[list[str]] = mapped_column(ARRAY(String), nullable = False)
    period : Mapped[int] = mapped_column(Integer, nullable = False)
    last_resolved_action_id : Mapped[int] = mapped_column(Integer, default = 0, nullable = False)
    paths_to_download : Mapped[list[str]] = mapped_column(ARRAY(String), default = [], nullable = False)