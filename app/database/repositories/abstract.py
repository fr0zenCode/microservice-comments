from abc import ABC, abstractmethod

from app.database.schemas import CommentSchemaAdd


class AbstractCommentsRepository(ABC):

    @abstractmethod
    async def add_comment(self, comment: CommentSchemaAdd):
        raise NotImplementedError

    @abstractmethod
    async def get_comment_by_id(self, comment_id: int):
        raise NotImplementedError

    @abstractmethod
    async def delete_comment_by_id(self, comment_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_all_comments_by_post_id(self, post_id: int):
        raise NotImplementedError
