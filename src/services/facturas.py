from managers.facturas import invoice_manager

from config.settings import logger

from schemas.facturas import AddFacturaSchema
from utils.response import ResponseHandler


class InvoiceService:
    """Class to struct responses from database."""

    def _struct_response(self, data):
        """Method to struct the data."""
        logger.info("InvoiceService | _struct_response(): STARTED...")
        response_list = []
        for item in data:
            info_structured = {
                "id": item.id,
                "fecha_emision": item.fecha_emision.isoformat()
                if item.fecha_emision
                else None,
                "fecha_vencimiento": item.fecha_vencimiento.isoformat()
                if item.fecha_vencimiento
                else None,
                "concepto": item.concepto,
                "monto": float(item.monto),
                "monto_pagado": float(item.monto_pagado),
                "estatus": item.estatus,
                "id_estudiante": item.id_estudiante,
            }

            response_list.append(info_structured)

        logger.success("InvoiceService | _struct_response(): FINISHED")
        return response_list

    def create_new_invoice(self, data: AddFacturaSchema):
        """Method to control flow during insert to db."""
        logger.info("InvoiceService | create_new_invoice(): STARTED...")

        response = invoice_manager.insert_new_invoice(model_data=data)

        logger.success("InvoiceService | create_new_invoice(): FINISHED")
        if len(response) > 0:
            structured_data = self._struct_response(data=response)

            return ResponseHandler.success(
                body=structured_data,
                status_code=201,
                pagination={
                    "total": len(response),
                    "next": None,
                    "previous": None,
                    "total_pages": 1,
                    "current_page": 1,
                },
            )

        else:
            return ResponseHandler.error(
                message=f"New invoice '{data.id}-{data.monto}-{data.concepto}' was not created! Please retry...",
                status_code=400,
            )

    def list_invoices(self, struct_response: bool = True, **filters):
        """Method to control response from request SELECT in database."""
        logger.info("InvoiceService | list_invoices(): STARTED...")
        response = invoice_manager.get_invoices(**filters)
        if len(response) > 0:
            if struct_response is True:
                structured_data = self._struct_response(data=response)

            logger.success("InvoiceService | list_invoices(): FINISHED")
            return ResponseHandler.success(
                body=structured_data,
                status_code=200,
                pagination={
                    "total": len(response),
                    "next": None,
                    "previous": None,
                    "total_pages": 1,
                    "current_page": 1,
                },
            )

        logger.success("InvoiceService | list_invoices(): FINISHED")
        return ResponseHandler.success(
            body=[],
            status_code=200,
            pagination={
                "total": 0,
                "next": None,
                "previous": None,
                "total_pages": 1,
                "current_page": 1,
            },
        )


invoice_service = InvoiceService()
