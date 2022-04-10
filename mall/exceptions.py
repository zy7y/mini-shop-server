from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        {"detail": exc.detail}, status_code=exc.status_code, headers=exc.headers
    )


exception_handlers = {HTTPException: http_exception}
