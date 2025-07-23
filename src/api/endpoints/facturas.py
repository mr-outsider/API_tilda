from fastapi import APIRouter

from config.settings import logger
from schemas.facturas import GetFacturaFilters, UpdateFacturaSchema
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


@router.delete("/{id_factura}")
async def delete_factura(id_factura: str):
    """Delete a  from db.

    Args:
        id_factura (str): Id in database
    """
    if len(id_factura) != 36:
        return ResponseHandler.error(
            message=f"length invoice id '{id_factura}' is not valid!", status_code=400
        )

    logger.info("Delete a invoice in progress... - STATUS: STARTED")
    response_invoice = invoice_service.delete_invoice(identificador=id_factura)
    logger.success("Delete a invoice finished - STATUS: OK")
    return response_invoice


@router.patch("/{id_invoice}")
async def update_factura(id_invoice: str, update_data: UpdateFacturaSchema):
    """Update a invoice from db.

    Args:
        id_invoice (str): Id in database
    """
    if len(id_invoice) != 36:
        return ResponseHandler.error(
            message=f"length invoice id '{id_invoice}' is not valid!", status_code=400
        )
    logger.info("Updating invoice in progress... - STATUS: STARTED")

    data_to_update = {}
    for field, value in update_data.dict(exclude_unset=True).items():
        if field == "estatus":
            valid_options = ["pendiente", "pagada", "vencida"]
            if value not in valid_options:
                return ResponseHandler.error(
                    message=f"estatus '{value}' is not a valid option. Please select a value in: {valid_options}",
                    status_code=400,
                )
        data_to_update[field] = value

    response = invoice_service.update_invoice(identificador=id_invoice, data=update_data)
    logger.success("Updating invoice finished - STATUS: FINISHED")

    return response
