from pydantic import BaseModel


class CommentToDB(BaseModel):
    post_id: int
    author_id: str
    comment_text: str


class CommentFullModel(CommentToDB):
    comment_id: int
