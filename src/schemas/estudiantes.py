from pydantic import BaseModel, constr
from typing import Optional, Literal
from datetime import date
from uuid import uuid4
from fastapi import Query


class AddEstudianteSchema(BaseModel):
    id: Optional[str] = str(uuid4())
    nombre: constr(max_length=100)
    apellido_paterno: constr(max_length=100)
    apellido_materno: constr(max_length=100)
    fecha_nacimiento: date
    genero: Literal["femenino", "masculino", "otro"]
    curp: constr(max_length=18)
    fecha_inscripcion: date
    grado_escolar: constr(max_length=50)
    especialidad: Optional[constr(max_length=255)] = None
    promedio_general: Optional[float] = None
    carrera: Optional[constr(max_length=150)] = None
    id_escuela: Optional[str] = None


class GetEstudianteFilters(BaseModel):
    id: Optional[str] = Query(None, max_length=36)
    curp: Optional[str] = Query(None, max_length=18)
    genero: Optional[str] = Query(None, max_length=20)
    id_escuela: Optional[str] = Query(None)
