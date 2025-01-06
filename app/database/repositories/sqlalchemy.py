from dataclasses import dataclass

from sqlalchemy import insert, select, delete

from app.database.core.engine import async_session_factory
from app.database.core.models import Comments
from app.database.repositories.abstract import AbstractCommentsRepository
from app.database.schemas import CommentSchemaAdd


@dataclass
class SQLAlchemyCommentsRepository(AbstractCommentsRepository):

    _async_session_factory: async_session_factory = async_session_factory

    async def add_comment(self, comment: CommentSchemaAdd):
        async with self._async_session_factory() as session:
            stmt = insert(Comments).values(
                author_id=comment.author_id,
                post_id=comment.post_id,
                text=comment.comment_text
            ).returning(Comments.id)
            added_comment_id = await session.execute(stmt)
            await session.commit()
            return added_comment_id.scalar_one()

    async def get_comment_by_id(self, comment_id: int):
        async with self._async_session_factory() as session:
            stmt = select(Comments).where(Comments.id == comment_id)
            comment = await session.execute(stmt)
            return comment.scalar_one().convert_to_pydantic_model()

    async def delete_comment_by_id(self, comment_id: int):
        async with self._async_session_factory() as session:
            stmt = delete(Comments).where(Comments.id == comment_id)
            await session.execute(stmt)
            await session.commit()

    async def get_all_comments_by_post_id(self, post_id: int):
        async with self._async_session_factory() as session:
            stmt = select(Comments).where(Comments.post_id == post_id)
            comments = await session.execute(stmt)
            comments_as_pydantic_models = [result.convert_to_pydantic_model() for result in comments.scalars()]
            return comments_as_pydantic_models


def get_sql_alchemy_comments_repository():
    return SQLAlchemyCommentsRepository()
