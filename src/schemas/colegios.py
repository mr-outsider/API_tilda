from pydantic import BaseModel, EmailStr, constr
from uuid import uuid4
from typing import Optional, Literal
from fastapi import Query


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


class GetColegioFilters(BaseModel):
    clave_cct: Optional[str] = Query(None, max_length=20)
    nombre: Optional[str] = Query(None, max_length=255)
    nivel_educativo: Optional[str] = Query(None)
    turno: Optional[str] = Query(None)
    estatus: Optional[str] = Query(None)
    correo_electronico: Optional[str] = Query(None)


class UpdateColegioSchema(BaseModel):
    nombre: Optional[constr(max_length=255)] = None
    calle: Optional[constr(max_length=255)] = None
    colonia: Optional[constr(max_length=255)] = None
    municipio: Optional[constr(max_length=100)] = None
    estado: Optional[constr(max_length=100)] = None
    codigo_postal: Optional[constr(max_length=10)] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    telefono: Optional[constr(max_length=20)] = None
    correo_electronico: Optional[EmailStr] = None
    nombre_director: Optional[constr(max_length=255)] = None
    turno: Optional[Literal["Matutino", "Vespertino", "Mixto"]] = None
    estatus: Optional[Literal["activa", "suspendida", "cerrada"]] = None
