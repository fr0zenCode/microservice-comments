from dataclasses import dataclass

from fastapi import Request, HTTPException


@dataclass
class AuthService:

    @staticmethod
    def get_bearer_from_request_header(self, request: Request, header_for_search: str = "Authorization"):
        token = request.headers.get(header_for_search)
        if token and token.startswith("Bearer "):
            return token.split(" ", 1)[1]
        raise HTTPException(status_code=401, detail="Not authorized.")

    def get_token_from_cookie(self, request):
        ...

    def decode_token(self, token):
        ...

    def encode_token(self, payload):
        ...

    def authorize_request(self, request, bearer_mode=False, cookie_mode=True):
        ...

