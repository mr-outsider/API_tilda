from pydantic import BaseModel, constr
from typing import Optional, Literal
from uuid import uuid4
from datetime import date
from fastapi import Query


class AddFacturaSchema(BaseModel):
    id: Optional[str] = str(uuid4())
    fecha_emision: date
    fecha_vencimiento: date
    concepto: constr(max_length=255)
    monto: float
    monto_pagado: Optional[float] = 0.00
    estatus: Literal["pendiente", "pagada", "vencida"] = "pendiente"
    id_estudiante: Optional[str] = None


class GetFacturaFilters(BaseModel):
    id: Optional[str] = Query(None, max_length=36)
    estatus: Optional[str] = Query(None, max_length=20)
    id_estudiante: Optional[str] = Query(None)
