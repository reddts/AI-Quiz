from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


def add_security_headers_middleware(app: FastAPI):
    """
    添加安全头的中间件

    :param app: FastAPI对象
    :return:
    """
    class SecurityHeadersMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            response: Response = await call_next(request)
            # 添加 X-Content-Type-Options 头
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response

    app.add_middleware(SecurityHeadersMiddleware)