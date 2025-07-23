from fastapi.responses import JSONResponse
from typing import Any, Optional, Dict, Union


class ResponseHandler:
    @staticmethod
    def success(
        body: Any,
        status_code: int = 200,
        pagination: Optional[Dict[str, Union[str, int]]] = None,
        message: Optional[str] = None,
    ) -> JSONResponse:
        response = {
            "status": "success",
        }
        if message:
            response["message"] = message
        if pagination:
            response["pagination"] = pagination

        response["body"] = body
        return JSONResponse(status_code=status_code, content=response)

    @staticmethod
    def error(
        message: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None,
    ) -> JSONResponse:
        response = {
            "status": "error",
            "error": message,
        }
        if details:
            response["details"] = details

        return JSONResponse(status_code=status_code, content=response)
