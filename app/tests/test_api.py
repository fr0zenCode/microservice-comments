from fastapi import APIRouter
from starlette.responses import Response

test_router = APIRouter(prefix="/test", tags=["For TESTs"])


@test_router.post("/simple-cookie-auth")
async def simple_cookie_auth(response: Response):
    """
    Отладочная функция. Кладет в куку токен.

    :param response: Ответ от сервера.
    :return: Словарь
    """
    response.set_cookie(key="token", value="Congratulations! You've get the token from cookies")
    return {"message": "successful"}


@test_router.post("/delete-test-token-from-cookies")
async def delete_test_token_from_cookies(response: Response):
    response.delete_cookie(key="token")
    return {"message": "token deleted"}
