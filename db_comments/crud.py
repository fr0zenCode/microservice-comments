from typing import Callable
import asyncio

from asyncpg import exceptions
from sqlalchemy import text, exc
from starlette.responses import JSONResponse

from db_comments.engine import async_session_factory
from db_comments.models import Comments
from db_comments.schemas import CommentToDB, CommentFullModel


class CommentsCRUD:

    TABLE_NAME = "comments"

    def __init__(self, session_factory: Callable = async_session_factory()):
        self._session_factory = session_factory

    def get_session_factory(self):
        return self._session_factory

    async def _get_items_from_db(self, where_params):
        async with self.get_session_factory() as session:
            stmt = text(f"""SELECT * FROM {self.TABLE_NAME} WHERE {where_params};""")
            q_result = await session.execute(stmt)
            return q_result

    async def add_comment(self, comment_for_add: CommentToDB) -> JSONResponse:

        new_comment = Comments(
            author_id=comment_for_add.author_id,
            post_id=comment_for_add.post_id,
            text=comment_for_add.comment_text
        )

        async with self.get_session_factory() as session:
            session.add(new_comment)
            try:
                await session.commit()
                return JSONResponse(content={"message": "successful. Comment was added."}, status_code=200)
            except (exceptions.InterfaceError, OSError):
                print("microservice-comments/db_comments/crud.py/def add_comment::::database error, didn't commit")
                return JSONResponse(content={"message": "unsuccessful, comment wasn't added"}, status_code=400)

    async def delete_comment_by_id(self, comment_id: int) -> JSONResponse:
        async with self.get_session_factory() as session:
            stmt = text(f"""DELETE FROM {self.TABLE_NAME} WHERE {self.TABLE_NAME}.comment_id = :comment_id;""")
            try:
                await session.execute(stmt, {"comment_id": comment_id})
                await session.commit()
                return JSONResponse(content={"message": f"comment with id {comment_id} was successfully deleted."})
            except (exceptions.InterfaceError, OSError):
                print("microservice-comments/db_comments/crud.py/def delete_comment_by_id"
                      "::::database error, didn't delete")
                return JSONResponse(content={"message": "unsuccessful, comment wasn't deleted"}, status_code=400)

    async def get_all_comments_for_post_by_post_id(self, post_id: int) -> [CommentFullModel]:
        sql_params = f"{self.TABLE_NAME}.post_id = {post_id}"
        r = await self._get_items_from_db(where_params=sql_params)
        rows = r.all()
        res = [
            CommentFullModel(comment_id=row[0], post_id=row[1], author_id=row[3], comment_text=row[2]) for row in rows
        ]
        return res

    async def get_all_comments_by_author_id(self, author_id: str):
        sql_params = f"{self.TABLE_NAME}.author_id = '{author_id}'"
        r = await self._get_items_from_db(where_params=sql_params)
        rows = r.all()
        res = [
            CommentFullModel(comment_id=row[0], post_id=row[1], author_id=row[3], comment_text=row[2]) for row in rows
        ]
        return res

    async def get_comment_by_id(self, comment_id: int):
        sql_params = f"{self.TABLE_NAME}.comment_id = {comment_id}"
        r = await self._get_items_from_db(where_params=sql_params)

        try:
            res = r.one()
            return CommentFullModel(comment_id=res[0], post_id=res[1], author_id=res[3], comment_text=res[2])
        except exc.NoResultFound:
            return JSONResponse(content={"message": "comment wasn't found"}, status_code=400)


comment_crud = CommentsCRUD()
