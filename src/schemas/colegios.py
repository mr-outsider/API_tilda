from pydantic import BaseModel, EmailStr, constr
from uuid import uuid4
from typing import Optional, Literal


class AddColegioSchema(BaseModel):
    id: Optional[str] = str(uuid4())
    clave_cct: constr(max_length=20)
    nombre: constr(max_length=255)
    nivel_educativo: Literal["Preescolar", "Primaria", "Secundaria", "Universidad"]
    calle: constr(max_length=255)
    colonia: constr(max_length=255)
    municipio: constr(max_length=100)
    estado: constr(max_length=100)
    codigo_postal: constr(max_length=10)
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    telefono: Optional[constr(max_length=20)] = None
    correo_electronico: EmailStr
    nombre_director: constr(max_length=255)
    turno: Literal["Matutino", "Vespertino", "Mixto"]
    estatus: Literal["activa", "suspendida", "cerrada"]

    # TODO: Cambiar el formato del error de los campos que se válidan con el schema
    # nivel_educativo, turno, estatus
