from pydantic import BaseModel, constr
from typing import Optional
from uuid import uuid4
from datetime import date


class AddFacturaSchema(BaseModel):
    id: Optional[str] = str(uuid4())
    fecha_emision: date
    fecha_vencimiento: date
    concepto: constr(max_length=255)
    monto: float
    monto_pagado: Optional[float] = 0.00
    estatus: constr(max_length=20) = "pendiente"
    id_estudiante: Optional[str] = None
