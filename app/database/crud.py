from abc import ABC, abstractmethod
from dataclasses import dataclass

import sqlalchemy
from asyncpg import exceptions
from sqlalchemy import exc, insert, select, delete
from starlette.responses import JSONResponse

from app.database.engine import async_session_factory
from app.database.models import Comments
from app.database.schemas import CommentSchemaAdd, CommentSchema


class AbstractCommentsCRUD(ABC):
    @abstractmethod
    async def add_comment(self, comment_for_add: CommentSchemaAdd):
        ...

    @abstractmethod
    async def get_comment_by_id(self, comment_id: int):
        ...

    @abstractmethod
    async def delete_comment_by_id(self, comment_id: int):
        ...

    @abstractmethod
    async def get_all_comments_by_post_id(self, post_id: int):
        ...


@dataclass
class CommentsCRUD(AbstractCommentsCRUD):

    session_factory = async_session_factory

    async def add_comment(self, comment_for_add: CommentSchemaAdd) -> int | JSONResponse:

        async with self.session_factory() as session:
            try:
                stmt = insert(Comments).values(
                    author_id=comment_for_add.author_id,
                    post_id=comment_for_add.post_id,
                    text=comment_for_add.comment_text
                ).returning(Comments.id)

                added_comment_id = await session.execute(stmt)
                await session.commit()
                new_comment_id = added_comment_id.scalar_one()
                print(f"INFO:       Добавлен комментарий с ID: {new_comment_id}")
                return new_comment_id
            except (exceptions.InterfaceError, OSError):
                print("ERROR:       microservice-comments/database"
                      "/crud.py/def add_comment::::database error, didn't commit")
                return JSONResponse(content={"message": "unsuccessful, comment not added"}, status_code=400)

    async def get_comment_by_id(self, comment_id: int) -> CommentSchema | JSONResponse:
        async with self.session_factory() as session:
            try:
                stmt = select(Comments).where(Comments.id == comment_id)
                comment = await session.execute(stmt)
                return comment.scalar_one().convert_to_pydantic_model()
            except sqlalchemy.exc.NoResultFound:
                print("No results")
                return JSONResponse(content={"message": "unsuccessful, not found"}, status_code=400)
            except (sqlalchemy.exc.InterfaceError, OSError):
                print("ERROR:       microservice-comments/database"
                      "/crud.py/def get_comment_by_id::::database error")
                return JSONResponse(content={"message": "database is not available"}, status_code=400)

    async def delete_comment_by_id(self, comment_id: int) -> JSONResponse:
        async with self.session_factory() as session:
            try:
                stmt = delete(Comments).where(Comments.id == comment_id)
                await session.execute(stmt)
                await session.commit()
                return JSONResponse(content={"message": "successful"}, status_code=200)
            except (sqlalchemy.exc.InterfaceError, OSError):
                print("ERROR:       microservice-comments/database"
                      "/crud.py/def delete_comment_by_id::::database error")
                return JSONResponse(content={"message": "database is not available"}, status_code=400)

    async def get_all_comments_by_post_id(self, post_id: int):
        async with self.session_factory() as session:
            try:
                stmt = select(Comments).where(Comments.post_id == post_id)
                results_from_db = await session.execute(stmt)
                results_for_use = [result.convert_to_pydantic_model() for result in results_from_db.scalars()]
                return results_for_use
            except (sqlalchemy.exc.InterfaceError, OSError):
                print("ERROR:       microservice-comments/database"
                      "/crud.py/def get_all_comments_by_post_id::::database error")
                return JSONResponse(content={"message": "database is not available"}, status_code=400)


def get_comment_crud() -> CommentsCRUD:
    """Фабрика для создания экземпляра класса для взаимодействия CRUD с БД с таблицей "comments"."""
    return CommentsCRUD()
