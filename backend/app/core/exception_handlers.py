from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException
from app.core.exceptions import DuplicateEmailError
from app.core.exceptions import ResourceNotFoundError
from app.core.exceptions import AuthorizationError
from app.core.exceptions import ValidationError
from app.core.exceptions import WorkflowExecutionError


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    if isinstance(exc, ResourceNotFoundError):
        status_code = 404

    elif isinstance(exc, AuthorizationError):
        status_code = 403

    elif isinstance(exc, DuplicateEmailError):
        status_code = 409

    elif isinstance(exc, ValidationError):
        status_code = 400

    elif isinstance(exc, WorkflowExecutionError):
        status_code = 400

    else:
        status_code = 500

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )