from sqlalchemy import Column, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database_models.estudiantes_model import EstudianteModel
from uuid import uuid4


from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class FacturaModel(Base):
    __tablename__ = "facturas"
    __table_args__ = {"schema": "public"}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    fecha_emision = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    concepto = Column(String(255), nullable=False)
    monto = Column(DECIMAL(10, 2), nullable=False)
    monto_pagado = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    estatus = Column(String(20), nullable=False, default="pendiente")
    id_estudiante = Column(
        String(36), ForeignKey(EstudianteModel.id, ondelete="CASCADE"), nullable=True
    )
    estudiante = relationship(
        EstudianteModel,
        backref="facturas",
        primaryjoin=id_estudiante == EstudianteModel.id,
    )
