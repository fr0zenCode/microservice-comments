from typing import Annotated

from fastapi import APIRouter, Request, Depends

from app.database.repositories.sqlalchemy import get_sql_alchemy_comments_repository
from app.database.schemas import CommentSchemaAdd, CommentSchema
from app.services.comments import get_comments_service, CommentsService


comments_router = APIRouter(prefix="/comments", tags=["Comments API's"])


@comments_router.post("/add-comment")
async def add_comment(
        request: Request,
        comment: CommentSchemaAdd,
        comments_service: Annotated[CommentsService, Depends(get_comments_service)]
) -> dict:
    """
    API для добавления нового комментария. Создает экземпляр сервиса комментариев из фабрики.
    Обращается к сервису комментариев для добавления нового комментария. \n
    """
    comment_id = await comments_service.add_comment(
        comment=comment,
        request=request,
        comments_repository=get_sql_alchemy_comments_repository()
    )
    return {"message": f"comment with id {comment_id} successfully added!"}


@comments_router.get("/get-comment-by-id")
async def get_comment(
        comment_id: int,
        comments_service: Annotated[CommentsService, Depends(get_comments_service)]
) -> CommentSchema:
    comment = await comments_service.get_comment_by_id(comment_id=comment_id)
    return comment


@comments_router.post("/delete-comment")
async def delete_comment(
        request: Request,
        comment_id: int,
        comments_service: Annotated[CommentsService, Depends(get_comments_service)]
) -> dict:
    await comments_service.delete_comment_by_id(request=request, comment_id=comment_id)
    return {"message": f"commend with id {comment_id} successfully deleted!"}


@comments_router.get("/get-comments-for-post")
async def get_comments_for_post(
        post_id: int,
        comments_service: Annotated[CommentsService, Depends(get_comments_service)]
) -> list[CommentSchema]:
    comments = await comments_service.get_all_comments_for_post_by_post_id(
        post_id=post_id,
        comments_repository=get_sql_alchemy_comments_repository()
    )
    return comments
