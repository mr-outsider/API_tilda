from database_models.colegio_model import ColegioModel
from config.manage_session import manage_connection
from schemas.colegios import AddColegioSchema
from config.settings import logger


class SchoolManager:
    """Class to struct responses from database."""

    def __init__(self, connection: object = None):
        self.connection = connection

    @manage_connection
    def get_schools(self, **filters):
        """Method to request register from table colegios in database."""
        logger.info("SchoolManager | get_schools(): STARTED...")

        clave_cct = filters.pop("clave_cct", None)
        nombre = filters.pop("nombre", None)
        nivel_educativo = filters.pop("nivel_educativo", None)
        turno = filters.pop("turno", None)
        estatus = filters.pop("estatus", None)
        correo_electronico = filters.pop("correo_electronico", None)

        try:
            query = self.connection.query(ColegioModel)
            if clave_cct:
                query = query.filter(ColegioModel.clave_cct == clave_cct)
            if nombre:
                query = query.filter(ColegioModel.nombre == nombre)
            if nivel_educativo:
                query = query.filter(ColegioModel.nivel_educativo == nivel_educativo)
            if turno:
                query = query.filter(ColegioModel.turno == turno)
            if estatus:
                query = query.filter(ColegioModel.estatus == estatus)
            if correo_electronico:
                query = query.filter(
                    ColegioModel.correo_electronico == correo_electronico
                )
            logger.success("SchoolManager | get_schools(): FINISHED")
            return query.all()
        except Exception as e:
            logger.error(f"SchoolManager | get_schools(): ERROR - {e}")
            self.connection.close()
            return []

    @manage_connection
    def insert_new_school(self, model_data: AddColegioSchema):
        """Method to insert a new register in colegios table."""
        logger.info("SchoolManager | insert_new_school(): STARTED...")
        try:
            school_obj = ColegioModel(
                id=model_data.id,
                clave_cct=model_data.clave_cct,
                nombre=model_data.nombre,
                nivel_educativo=model_data.nivel_educativo,
                calle=model_data.calle,
                colonia=model_data.colonia,
                municipio=model_data.municipio,
                estado=model_data.estado,
                codigo_postal=model_data.codigo_postal,
                latitud=model_data.latitud,
                longitud=model_data.longitud,
                telefono=model_data.telefono,
                correo_electronico=model_data.correo_electronico,
                nombre_director=model_data.nombre_director,
                turno=model_data.turno,
                estatus=model_data.estatus,
            )
            self.connection.add(school_obj)
            self.connection.commit()
            self.connection.refresh(school_obj)
            logger.success("SchoolManager | insert_new_school(): FINISHED")
            return [school_obj]
        except Exception as e:
            self.connection.rollback()
            logger.error(f"SchoolManager | insert_new_school(): ERROR - {e}")
            self.connection.close()
            return []


school_manager = SchoolManager()
