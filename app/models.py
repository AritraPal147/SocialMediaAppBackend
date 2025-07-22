from sqlalchemy import TIMESTAMP, Boolean, Integer, String, false, null, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String, nullable=False)
    content = mapped_column(String, nullable=False)
    published = mapped_column(Boolean, default=True, server_default=text("true"))
    created_at = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
