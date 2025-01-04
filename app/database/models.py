from sqlalchemy.orm import Mapped, mapped_column

from .engine import Base
from .schemas import CommentSchema


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author_id: Mapped[int]
    post_id: Mapped[int]
    text: Mapped[str]

    def convert_to_pydantic_model(self) -> CommentSchema:
        return CommentSchema(
            id=self.id,
            author_id=self.author_id,
            post_id=self.post_id,
            text=self.text
        )
