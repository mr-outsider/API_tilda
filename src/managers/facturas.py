from database_models.facturas_model import FacturaModel
from config.manage_session import manage_connection
from schemas.facturas import AddFacturaSchema
from config.settings import logger


class InvoiceManager:
    """Class to struct responses from database."""

    def __init__(self, connection: object = None):
        self.connection = connection

    @manage_connection
    def insert_new_invoice(self, model_data: AddFacturaSchema):
        """Method to insert a new register in facturas table."""
        logger.info("InvoiceManager | insert_new_invoice(): STARTED...")

        try:
            invoice_obj = FacturaModel(
                id=model_data.id,
                fecha_emision=model_data.fecha_emision,
                fecha_vencimiento=model_data.fecha_vencimiento,
                concepto=model_data.concepto,
                monto=model_data.monto,
                monto_pagado=model_data.monto_pagado,
                estatus=model_data.estatus,
                id_estudiante=model_data.id_estudiante,
            )
            self.connection.add(invoice_obj)
            self.connection.commit()
            self.connection.refresh(invoice_obj)
            logger.success("InvoiceManager | insert_new_invoice(): FINISHED")
            return [invoice_obj]
        except Exception as e:
            self.connection.rollback()
            logger.error(f"InvoiceManager | insert_new_invoice(): ERROR - {e}")
            self.connection.close()
            return []

    @manage_connection
    def get_invoices(self, **filters):
        """Method to request register from table invoices in database."""
        logger.info("InvoiceManager | get_invoices(): STARTED...")

        id_obj = filters.pop("id", None)
        estatus = filters.pop("estatus", None)
        id_estudiante = filters.pop("id_estudiante", None)

        try:
            query = self.connection.query(FacturaModel)
            if id_obj:
                query = query.filter(FacturaModel.id == id_obj)
            if estatus:
                query = query.filter(FacturaModel.estatus == estatus)
            if id_estudiante:
                query = query.filter(FacturaModel.id_estudiante == id_estudiante)

            logger.success("InvoiceManager | get_invoices(): FINISHED")
            return query.all()
        except Exception as e:
            logger.error(f"InvoiceManager | get_invoices(): ERROR - {e}")
            self.connection.close()
            return []


invoice_manager = InvoiceManager()
