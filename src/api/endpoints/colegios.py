from fastapi import APIRouter

from config.settings import logger
from schemas.colegios import AddColegioSchema
from services.colegios import school_service


router = APIRouter(prefix="/schools")


# POST /brands
@router.post("")
async def add_colegio(colegio: AddColegioSchema):
    """Add a new school to db."""
    logger.info("Create a new school in progress... - STATUS: STARTED")
    response_school = school_service.create_new_school(data=colegio)
    logger.success("Create a new school finished - STATUS: OK")
    return response_school
