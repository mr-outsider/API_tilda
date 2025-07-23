from sqlalchemy import Column, String, Numeric

from sqlalchemy.ext.declarative import declarative_base

import uuid

Base = declarative_base()


class ColegioModel(Base):
    __tablename__ = "colegios"
    __table_args__ = {"schema": "public"}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clave_cct = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    nivel_educativo = Column(String(50), nullable=False)
    calle = Column(String(255), nullable=False)
    colonia = Column(String(255), nullable=False)
    municipio = Column(String(100), nullable=False)
    estado = Column(String(100), nullable=False)
    codigo_postal = Column(String(10), nullable=False)
    latitud = Column(Numeric(9, 6), nullable=True)
    longitud = Column(Numeric(9, 6), nullable=True)
    telefono = Column(String(20), nullable=True)
    correo_electronico = Column(String(100), unique=True, nullable=False)
    nombre_director = Column(String(255), nullable=False)
    turno = Column(String(20), nullable=False)
    estatus = Column(String(20), nullable=False)
