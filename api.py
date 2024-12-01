from fastapi import APIRouter
from starlette.responses import JSONResponse

from db_comments.crud import comment_crud
from db_comments.schemas import CommentToDB

comments_router = APIRouter(prefix="/comments", tags=["Comments API's"])


@comments_router.post("/add-comment")
async def add_comment(comment: CommentToDB) -> JSONResponse:
    response = await comment_crud.add_comment(comment)
    return response


@comments_router.post("/delete-comment")
async def delete_comment(comment_id: int) -> JSONResponse:
    response = await comment_crud.delete_comment_by_id(comment_id)
    return response


@comments_router.get("/get-comments-for-post")
async def get_comments_for_post(post_id: int):
    res = await comment_crud.get_all_comments_for_post_by_post_id(post_id)
    return res


@comments_router.get("/get-comments-for-author-by-id")
async def get_comments_for_post(author_id: str):
    res = await comment_crud.get_all_comments_by_author_id(author_id=author_id)
    return res


@comments_router.get("/get-comment")
async def get_comment(comment_id: int):
    res = await comment_crud.get_comment_by_id(comment_id)
    return res
