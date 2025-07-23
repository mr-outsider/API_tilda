from database_models.estudiantes_model import EstudianteModel
from config.manage_session import manage_connection
from schemas.estudiantes import AddEstudianteSchema
from config.settings import logger


class StudentManager:
    """Class to struct responses from database."""

    def __init__(self, connection: object = None):
        self.connection = connection

    @manage_connection
    def get_students(self, **filters):
        """Method to request register from table colegios in database."""
        logger.info("StudentManager | get_students(): STARTED...")

        id_obj = filters.pop("id", None)
        curp = filters.pop("curp", None)
        id_escuela = filters.pop("id_escuela", None)

        try:
            query = self.connection.query(EstudianteModel)
            if id_obj:
                query = query.filter(EstudianteModel.id == id_obj)
            if curp:
                query = query.filter(EstudianteModel.curp == curp)
            if id_escuela:
                query = query.filter(EstudianteModel.id_escuela == id_escuela)

            logger.success("StudentManager | get_students(): FINISHED")
            return query.all()
        except Exception as e:
            logger.error(f"StudentManager | get_students(): ERROR - {e}")
            self.connection.close()
            return []

    @manage_connection
    def insert_new_student(self, model_data: AddEstudianteSchema):
        """Method to insert a new register in estudiantes table."""
        logger.info("StudentManager | insert_new_student(): STARTED...")

        try:
            student_obj = EstudianteModel(
                id=model_data.id,
                nombre=model_data.nombre,
                apellido_paterno=model_data.apellido_paterno,
                apellido_materno=model_data.apellido_materno,
                fecha_nacimiento=model_data.fecha_nacimiento,
                genero=model_data.genero,
                curp=model_data.curp,
                fecha_inscripcion=model_data.fecha_inscripcion,
                grado_escolar=model_data.grado_escolar,
                especialidad=model_data.especialidad,
                promedio_general=model_data.promedio_general,
                carrera=model_data.carrera,
                id_escuela=model_data.id_escuela,
            )
            self.connection.add(student_obj)
            self.connection.commit()
            self.connection.refresh(student_obj)
            logger.success("StudentManager | insert_new_student(): FINISHED")
            return [student_obj]
        except Exception as e:
            self.connection.rollback()
            logger.error(f"StudentManager | insert_new_student(): ERROR - {e}")
            self.connection.close()
            return []

    @manage_connection
    def delete_student(self, **filters):
        """Method to delete a student by ID."""
        logger.info("SchoolManager | delete_student(): STARTED...")
        id_obj = filters.pop("id", None)
        curp = filters.pop("curp", None)

        try:
            if id_obj:
                student = (
                    self.connection.query(EstudianteModel).filter_by(id=id_obj).first()
                )
            if curp:
                student = (
                    self.connection.query(EstudianteModel).filter_by(curp=curp).first()
                )

            if not student:
                logger.warning(
                    f"SchoolManager | delete_student(): Student with ID {id_obj}|{curp} not found."
                )
                return []

            self.connection.delete(student)
            self.connection.commit()
            logger.success("SchoolManager | delete_student(): FINISHED")
            return [student]
        except Exception as e:
            self.connection.rollback()
            logger.error(f"SchoolManager | delete_student(): ERROR - {e}")
            self.connection.close()
            return []


student_manager = StudentManager()
