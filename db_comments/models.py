from sqlalchemy.orm import Mapped, mapped_column

from .engine import Base


class Comments(Base):
    __tablename__ = "comments"

    comment_id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[str]
    post_id: Mapped[int]
    text: Mapped[str]
