from managers.estudiantes import student_manager

from config.settings import logger

from schemas.estudiantes import AddEstudianteSchema, UpdateEstudianteSchema
from utils.response import ResponseHandler


class StudentService:
    """Class to struct responses from database."""

    def _struct_response(self, data):
        """Method to struct the data."""
        logger.info("StudentService | _struct_response(): STARTED...")
        response_list = []
        for item in data:
            info_structured = {
                "id": item.id,
                "nombre": item.nombre,
                "apellido_paterno": item.apellido_paterno,
                "apellido_materno": item.apellido_materno,
                "fecha_nacimiento": item.fecha_nacimiento.isoformat()
                if item.fecha_nacimiento
                else None,
                "genero": item.genero,
                "curp": item.curp,
                "fecha_inscripcion": item.fecha_inscripcion.isoformat()
                if item.fecha_inscripcion
                else None,
                "grado_escolar": item.grado_escolar,
                "especialidad": item.especialidad,
                "promedio_general": float(item.promedio_general)
                if item.promedio_general is not None
                else None,
                "carrera": item.carrera,
                "id_escuela": item.id_escuela,
            }

            response_list.append(info_structured)

        logger.success("StudentService | _struct_response(): FINISHED")
        return response_list

    def create_new_student(self, data: AddEstudianteSchema):
        """Method to control flow during insert to db."""
        logger.info("StudentService | create_new_student(): STARTED...")
        curp = data.curp
        filters = {"curp": curp}
        response = student_manager.get_students(**filters)
        if len(response) > 0:
            return ResponseHandler.error(
                message=f"Student '{curp}' already exist!", status_code=400
            )

        response = student_manager.insert_new_student(model_data=data)

        logger.success("StudentService | create_new_student(): FINISHED")
        if len(response) > 0:
            structured_data = self._struct_response(data=response)

            return ResponseHandler.success(
                body=structured_data,
                status_code=201,
                pagination={
                    "total": len(response),
                    "next": None,
                    "previous": None,
                    "total_pages": 1,
                    "current_page": 1,
                },
            )

        else:
            return ResponseHandler.error(
                message=f"New student '{curp}' was not created! Please retry...",
                status_code=400,
            )

    def list_students(self, struct_response: bool = True, **filters):
        """Method to control response from request SELECT in database."""
        logger.info("StudentService | list_student(): STARTED...")
        response = student_manager.get_students(**filters)
        if len(response) > 0:
            if struct_response is True:
                structured_data = self._struct_response(data=response)

            logger.success("StudentService | list_student(): FINISHED")
            return ResponseHandler.success(
                body=structured_data,
                status_code=200,
                pagination={
                    "total": len(response),
                    "next": None,
                    "previous": None,
                    "total_pages": 1,
                    "current_page": 1,
                },
            )

        logger.success("StudentService | list_student(): FINISHED")
        return ResponseHandler.success(
            body=[],
            status_code=200,
            pagination={
                "total": 0,
                "next": None,
                "previous": None,
                "total_pages": 1,
                "current_page": 1,
            },
        )

    def delete_student(self, identificador: str):
        """Method to control flow during delete from db."""
        logger.info("StudentService | delete_student(): STARTED...")

        if len(identificador) == 36:
            filters = {"id": identificador}
        elif len(identificador) <= 18:
            filters = {"curp": identificador}

        response = student_manager.delete_student(**filters)
        if len(response) == 0:
            return ResponseHandler.error(
                message=f"Student '{identificador}' was not deleted! Please check if the register exist.",
                status_code=400,
            )

        logger.success("StudentService | delete_student(): FINISHED")

        return ResponseHandler.success(
            message=f"Student '{identificador}' deleted OK!",
            body=[],
            status_code=200,
            pagination={
                "total": len(response),
                "next": None,
                "previous": None,
                "total_pages": 1,
                "current_page": 1,
            },
        )

    def update_student(self, identificador: str, data: UpdateEstudianteSchema):
        """Method to control flow during update."""
        logger.info("StudentService | update_student(): STARTED...")
        if len(identificador) == 36:
            student_id = identificador
            filters = {"id": identificador}
        elif len(identificador) <= 18:
            student_id = identificador
            filters = {"curp": identificador}

        response = student_manager.get_students(**filters)
        if len(response) == 0:
            return ResponseHandler.error(
                message=f"Student '{identificador}' does not exist!",
                status_code=400,
            )

        response = student_manager.update_student(student_id=student_id, model_data=data)

        if len(response) > 0:
            structured_data = self._struct_response(data=response)

            logger.success("StudentService | update_student(): FINISHED")
            return ResponseHandler.success(
                body=structured_data,
                status_code=200,
                pagination={
                    "total": len(response),
                    "next": None,
                    "previous": None,
                    "total_pages": 1,
                    "current_page": 1,
                },
            )

        return ResponseHandler.error(
            message=f"Student '{identificador}' was not updated! Please check if the register exist.",
            status_code=400,
        )


student_service = StudentService()
