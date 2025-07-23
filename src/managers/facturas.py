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


invoice_manager = InvoiceManager()
