from fastapi import APIRouter
from starlette.responses import JSONResponse

from database.crud import get_comment_crud
from database.schemas import CommentSchemaAdd


comments_router = APIRouter(prefix="/comments", tags=["Comments API's"])
comments_crud = get_comment_crud()


@comments_router.post("/add-comment")
async def add_comment(comment: CommentSchemaAdd):
    comment_id = await comments_crud.add_comment(comment)
    return {"comment_id": comment_id}


@comments_router.get("/get-comment")
async def get_comment(comment_id: int):
    res = await comments_crud.get_comment_by_id(comment_id)
    return res


@comments_router.post("/delete-comment")
async def delete_comment(comment_id: int) -> JSONResponse:
    response = await comments_crud.delete_comment_by_id(comment_id)
    return response


@comments_router.get("/get-comments-for-post")
async def get_comments_for_post(post_id: int):
    res = await comments_crud.get_all_comments_by_post_id(post_id=post_id)
    return res
