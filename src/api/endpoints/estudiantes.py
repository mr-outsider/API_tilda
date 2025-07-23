from fastapi import APIRouter

from config.settings import logger
from schemas.estudiantes import GetEstudianteFilters
from fastapi import Depends
from utils.response import ResponseHandler
from services.estudiantes import student_service


router = APIRouter(prefix="/students")


@router.get(
    "",
)
async def get_students(filters: GetEstudianteFilters = Depends()):
    """List all students from database"""
    logger.info("Getting students in progress... - STATUS: STARTED")

    filter_dict = {k: v for k, v in filters.dict().items() if v is not None}

    if "genero" in filter_dict:
        valid_options = ["femenino", "masculino", "otro"]
        if filter_dict["genero"] not in valid_options:
            value = filter_dict["genero"]
            return ResponseHandler.error(
                message=f"nivel_educativo '{value}' is not a valid option. Please select a value in: {valid_options}",
                status_code=400,
            )

    response = student_service.list_students(**filter_dict)
    logger.success("Getting students finished - STATUS: OK")
    return response
