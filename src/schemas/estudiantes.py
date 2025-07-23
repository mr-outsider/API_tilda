from pydantic import BaseModel, constr
from typing import Optional
from datetime import date
from uuid import uuid4


class AddEstudianteSchema(BaseModel):
    id: Optional[str] = str(uuid4())
    nombre: constr(max_length=100)
    apellido_paterno: constr(max_length=100)
    apellido_materno: constr(max_length=100)
    fecha_nacimiento: date
    genero: constr(max_length=20)
    curp: constr(max_length=18)
    fecha_inscripcion: date
    grado_escolar: constr(max_length=50)
    especialidad: Optional[constr(max_length=255)] = None
    promedio_general: Optional[float] = None
    carrera: Optional[constr(max_length=150)] = None
    id_escuela: Optional[str] = None
