from sqlalchemy import Column, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database_models.colegio_model import ColegioModel
from uuid import uuid4


from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class EstudianteModel(Base):
    __tablename__ = "estudiantes"
    __table_args__ = {"schema": "public"}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    genero = Column(String(20), nullable=False)
    curp = Column(String(18), nullable=False, unique=True)
    fecha_inscripcion = Column(Date, nullable=False)
    grado_escolar = Column(String(50), nullable=False)
    especialidad = Column(String(255), nullable=True)
    promedio_general = Column(DECIMAL(4, 2), nullable=True)
    carrera = Column(String(150), nullable=True)
    id_escuela = Column(String(36), ForeignKey(ColegioModel.id), nullable=False)
    escuela = relationship(
        ColegioModel, backref="estudiantes", primaryjoin=id_escuela == ColegioModel.id
    )
