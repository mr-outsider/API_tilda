from managers.colegios import school_manager

from config.settings import logger

from schemas.colegios import AddColegioSchema
from utils.response import ResponseHandler


class SchoolService:
    """Class to struct responses from database."""

    def _struct_response(self, data):
        """Method to struct the data."""
        logger.info("SchoolService | _struct_response(): STARTED...")
        response_list = []
        for item in data:
            filter = {"clave_cct": item.clave_cct}
            info = school_manager.get_schools(**filter)
            if len(info) > 0:
                info_structured = {
                    "id": info[0].id,
                    "clave_cct": info[0].clave_cct,
                    "nombre": info[0].nombre,
                    "nivel_educativo": info[0].nivel_educativo,
                    "calle": info[0].calle,
                    "colonia": info[0].colonia,
                    "municipio": info[0].municipio,
                    "estado": info[0].estado,
                    "codigo_postal": info[0].codigo_postal,
                    "latitud": float(info[0].latitud)
                    if info[0].latitud is not None
                    else None,
                    "longitud": float(info[0].longitud)
                    if info[0].longitud is not None
                    else None,
                    "telefono": info[0].telefono,
                    "correo_electronico": info[0].correo_electronico,
                    "nombre_director": info[0].nombre_director,
                    "turno": info[0].turno,
                    "estatus": info[0].estatus,
                }

                response_list.append(info_structured)

        logger.success("SchoolService | _struct_response(): FINISHED")
        return response_list

    def create_new_school(self, data: AddColegioSchema):
        """Method to control flow during insert to db."""
        # Check if brand exist
        logger.info("SchoolService | create_net_school(): STARTED...")
        clave_cct = data.clave_cct
        filters = {"clave_cct": clave_cct}
        response = school_manager.get_schools(**filters)
        if len(response) > 0:
            return ResponseHandler.error(
                message=f"School '{clave_cct}' already exist!", status_code=400
            )

        response = school_manager.insert_new_school(model_data=data)
        logger.success("SchoolService | create_net_school(): FINISHED")
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
                message=f"New School '{clave_cct}' was not created! Please retry...",
                status_code=400,
            )

    def list_colegios(self, struct_response: bool = True, **filters):
        """Method to control response from request SELECT in database."""
        logger.info("SchoolService | list_colegios(): STARTED...")
        response = school_manager.get_schools(**filters)
        if len(response) > 0:
            if struct_response is True:
                structured_data = self._struct_response(data=response)

            logger.success("SchoolService | list_colegios(): FINISHED")
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

        logger.success("SchoolService | list_colegios(): FINISHED")
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

    def delete_school(self, identificador: str):
        """Method to control flow during delete from db."""
        logger.info("SchoolService | delete_school(): STARTED...")

        if len(identificador) == 36:
            filters = {"id": identificador}
        elif len(identificador) <= 20:
            filters = {"clave_cct": identificador}

        response = school_manager.delete_school(**filters)
        if len(response) == 0:
            return ResponseHandler.error(
                message=f"School '{identificador}' was not deleted! Please check if the register exist.",
                status_code=400,
            )

        logger.success("SchoolService | delete_school(): FINISHED")

        return ResponseHandler.success(
            message=f"School '{identificador}' deleted OK!",
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

    def update_school(self, identificador: str, data: dict):
        """Method to control flow during update."""
        logger.info("SchoolSeervice | update_school(): STARTED...")
        if len(identificador) == 36:
            school_id = identificador
            filters = {"id": identificador}
        elif len(identificador) <= 20:
            school_id = identificador
            filters = {"clave_cct": identificador}

        response = school_manager.get_schools(**filters)
        if len(response) == 0:
            return ResponseHandler.error(
                message=f"School '{identificador}' does not exist!",
                status_code=400,
            )

        response = school_manager.update_school(school_id=school_id, model_data=data)

        if len(response) > 0:
            structured_data = self._struct_response(data=response)

            logger.success("SchoolService | update_school(): FINISHED")
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
            message=f"School '{identificador}' was not updated! Please check if the register exist.",
            status_code=400,
        )


school_service = SchoolService()
