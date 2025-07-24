from database_models.facturas_model import FacturaModel
from services.facturas import invoice_service
from unittest.mock import patch
from uuid import uuid4
from datetime import date
from decimal import Decimal


class TestServiceInvoceConfig:
    obj_invoice = FacturaModel(
        id=str(uuid4()),
        fecha_emision=date(2025, 1, 15),
        fecha_vencimiento=date(2025, 2, 15),
        concepto="Mensualidad enero",
        monto=Decimal("1200.00"),
        monto_pagado=Decimal("0.00"),
        estatus="pendiente",
        id_estudiante="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    )

    @patch("managers.facturas.InvoiceManager.get_invoices")
    def test_struct_response_invoice_service(self, mock_response):
        """Test _struct_response method."""
        mock_response.return_value = [self.obj_invoice]
        response = invoice_service._struct_response(data=[self.obj_invoice])

        assert isinstance(response, list)
        assert len(response) == 1
        assert response[0]["concepto"] == "Mensualidad enero"
        assert response[0]["estatus"] == "pendiente"
