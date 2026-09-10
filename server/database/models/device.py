from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from database.engine import Base

class Device(Base):
    __tablename__ = 'devices'
    device_id : Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    hostname : Mapped[str] = mapped_column(String, nullable = False)
    platform : Mapped[str] = mapped_column(String, nullable = False)
    mac : Mapped[list[str]] = mapped_column(ARRAY(String), nullable = False)
