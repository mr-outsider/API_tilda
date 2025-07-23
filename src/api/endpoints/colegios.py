from fastapi import APIRouter

from config.settings import logger
from schemas.colegios import AddColegioSchema, GetColegioFilters, UpdateColegioSchema
from schemas.estudiantes import AddEstudianteSchema
from services.colegios import school_service
from services.estudiantes import student_service
from fastapi import Depends
from utils.response import ResponseHandler
import json


router = APIRouter(prefix="/schools")


@router.post("")
async def add_colegio(colegio: AddColegioSchema):
    """Add a new school to db."""
    logger.info("Create a new school in progress... - STATUS: STARTED")
    colegio.nombre = colegio.nombre.title()
    response_school = school_service.create_new_school(data=colegio)
    logger.success("Create a new school finished - STATUS: OK")
    return response_school


@router.get(
    "",
)
async def get_colegios(filters: GetColegioFilters = Depends()):
    """List all colegios from database"""
    logger.info("Getting colegios in progress... - STATUS: STARTED")

    filter_dict = {k: v for k, v in filters.dict().items() if v is not None}

    if "nivel_educativo" in filter_dict:
        valid_options = ["Preescolar", "Primaria", "Secundaria", "Universidad"]
        if filter_dict["nivel_educativo"] not in valid_options:
            value = filter_dict["nivel_educativo"]
            return ResponseHandler.error(
                message=f"nivel_educativo '{value}' is not a valid option. Please select a value in: {valid_options}",
                status_code=400,
            )

    if "turno" in filter_dict:
        valid_options = ["Matutino", "Vespertino", "Mixto"]
        if filter_dict["turno"] not in valid_options:
            value = filter_dict["turno"]
            return ResponseHandler.error(
                message=f"turno '{value}' is not a valid option. Please select a value in: {valid_options}",
                status_code=400,
            )

    if "estatus" in filter_dict:
        valid_options = ["activa", "suspendida", "cerrada"]
        if filter_dict["estatus"] not in valid_options:
            value = filter_dict["estatus"]
            return ResponseHandler.error(
                message=f"turno '{value}' is not a valid option. Please select a value in: {valid_options}",
                status_code=400,
            )

    response = school_service.list_colegios(**filter_dict)
    logger.success("Getting colegios finished - STATUS: OK")
    return response


@router.delete("/{id_colegio}")
async def delete_colegion(id_colegio: str):
    """Delete a school from db.

    Args:
        id_colegio (str): Could be id in database or clave_cct
    """
    logger.info("Delete a school in progress... - STATUS: STARTED")
    response_school = school_service.delete_school(identificador=id_colegio)
    logger.success("Delete a school finished - STATUS: OK")
    return response_school


@router.patch("/{id_colegio}")
async def update_colegio(id_colegio: str, update_data: UpdateColegioSchema):
    """Update a school from db.

    Args:
        id_colegio (str): Could be id in database or clave_cct
    """
    logger.info("Updating model in progress... - STATUS: STARTED")

    data_to_update = {}
    for field, value in update_data.dict(exclude_unset=True).items():
        data_to_update[field] = value

    response = school_service.update_school(identificador=id_colegio, data=update_data)
    logger.success("Updating model finished - STATUS: FINISHED")

    return response


# Student
@router.post("/{id_colegio}/student")
async def add_estudiante(id_colegio: str, datos_estudiante: AddEstudianteSchema):
    """add a student linked to school.

    Args:
        id_colegio (str): clave_cct
    """
    logger.info("Create a new student in progress... - STATUS: STARTED")

    filter_dict = {"clave_cct": id_colegio}
    response = school_service.list_colegios(**filter_dict)

    if json.loads(response.body)["pagination"]["total"] != 1:
        return ResponseHandler.error(
            message=f"School '{id_colegio}' does not exist in database!", status_code=400
        )

    identificador_colegio = json.loads(response.body)["body"][0]["id"]
    datos_estudiante.id_escuela = identificador_colegio
    response_school = student_service.create_new_student(data=datos_estudiante)
    logger.success("Create a new student finished - STATUS: OK")
    return response_school
