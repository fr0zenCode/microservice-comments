from dataclasses import dataclass

from starlette.requests import Request

from app.database.crud import get_comment_crud
from app.database.schemas import CommentSchemaAdd


@dataclass
class CommentsService:

    comments_dto = get_comment_crud()

    # надо сделать механику авторизации

    async def add_comment(self, comment: CommentSchemaAdd, request: Request):
        print(request)
        await self.comments_dto.add_comment(comment_for_add=comment)


def get_comments_service():
    return CommentsService()
