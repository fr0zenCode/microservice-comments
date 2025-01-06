import uvicorn
from fastapi import FastAPI

from app.api.handlers import comments_router
from app.tests.test_api import test_router

app_comments = FastAPI()
app_comments.include_router(comments_router)
app_comments.include_router(test_router)


if __name__ == '__main__':
    uvicorn.run("main:app_comments", reload=True)
