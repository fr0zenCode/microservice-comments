from dataclasses import dataclass

from starlette.requests import Request

from app.database.repositories.abstract import AbstractCommentsRepository
from app.services.auth import AuthService
from app.database.schemas import CommentSchemaAdd


@dataclass
class CommentsService:

    auth_service = AuthService()

    async def add_comment(
            self,
            comment: CommentSchemaAdd,
            request: Request,
            comments_repository: AbstractCommentsRepository
    ):

        self.auth_service.authorize_request(request)
        new_comment_id = await comments_repository.add_comment(comment=comment)
        return new_comment_id

    async def delete_comment_by_id(
            self,
            request: Request,
            comment_id: int,
            comments_repository: AbstractCommentsRepository
    ):
        self.auth_service.authorize_request(request)
        await comments_repository.delete_comment_by_id(comment_id=comment_id)

    @staticmethod
    async def get_comment_by_id(comment_id: int, comments_repository: AbstractCommentsRepository):
        comment = await comments_repository.get_comment_by_id(comment_id=comment_id)
        return comment

    @staticmethod
    async def get_all_comments_for_post_by_post_id(
            post_id: int,
            comments_repository: AbstractCommentsRepository
    ):
        comments = await comments_repository.get_all_comments_by_post_id(post_id=post_id)
        return comments


def get_comments_service():
    return CommentsService()
