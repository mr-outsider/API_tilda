from fastapi import APIRouter

from config.settings import logger
from schemas.facturas import GetFacturaFilters
from fastapi import Depends
from utils.response import ResponseHandler
from services.facturas import invoice_service

router = APIRouter(prefix="/invoices")


@router.get(
    "",
)
async def get_factura(filters: GetFacturaFilters = Depends()):
    """List all invoices from database"""
    logger.info("Getting invoices in progress... - STATUS: STARTED")

    filter_dict = {k: v for k, v in filters.dict().items() if v is not None}
    if "estatus" in filter_dict:
        valid_options = ["pendiente", "pagada", "vencida"]
        if filter_dict["estatus"] not in valid_options:
            value = filter_dict["estatus"]
            return ResponseHandler.error(
                message=f"estatus '{value}' is not a valid option. Please select a value in: {valid_options}",
                status_code=400,
            )

    response = invoice_service.list_invoices(**filter_dict)
    logger.success("Getting invoices finished - STATUS: OK")
    return response
