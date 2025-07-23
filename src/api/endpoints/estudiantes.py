from fastapi import APIRouter

from config.settings import logger
from schemas.estudiantes import GetEstudianteFilters, UpdateEstudianteSchema
from fastapi import Depends
from utils.response import ResponseHandler
from services.estudiantes import student_service


router = APIRouter(prefix="/students")


@router.get(
    "",
)
async def get_estudiante(filters: GetEstudianteFilters = Depends()):
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


@router.delete("/{id_estudiante}")
async def delete_estudiante(id_estudiante: str):
    """Delete a  from db.

    Args:
        id_estudiante (str): Could be id in database or curp
    """
    if len(id_estudiante) != 36 and len(id_estudiante) > 18:
        return ResponseHandler.error(
            message=f"length student id '{id_estudiante}' is not valid!", status_code=400
        )

    logger.info("Delete a student in progress... - STATUS: STARTED")
    response_student = student_service.delete_student(identificador=id_estudiante)
    logger.success("Delete a student finished - STATUS: OK")
    return response_student


@router.patch("/{id_estudiante}")
async def update_colegio(id_estudiante: str, update_data: UpdateEstudianteSchema):
    """Update a student from db.

    Args:
        id_estudiante (str): Could be id in database or curp
    """
    if len(id_estudiante) != 36 and len(id_estudiante) > 18:
        return ResponseHandler.error(
            message=f"length student id '{id_estudiante}' is not valid!", status_code=400
        )
    logger.info("Updating model in progress... - STATUS: STARTED")

    data_to_update = {}
    for field, value in update_data.dict(exclude_unset=True).items():
        data_to_update[field] = value

    response = student_service.update_student(
        identificador=id_estudiante, data=update_data
    )
    logger.success("Updating model finished - STATUS: FINISHED")

    return response
