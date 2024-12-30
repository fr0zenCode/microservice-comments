from pydantic import BaseModel


class CommentSchema(BaseModel):
    id: int
    post_id: int
    author_id: int
    text: str


class CommentSchemaAdd(BaseModel):
    post_id: int
    author_id: int
    comment_text: str
