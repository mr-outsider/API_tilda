from fastapi import APIRouter

from .endpoints import health, colegios, estudiantes, facturas

api_router = APIRouter()
api_router.include_router(colegios.router, tags=["school_crud"])
api_router.include_router(estudiantes.router, tags=["students_crud"])
api_router.include_router(facturas.router, tags=["invoices_crud"])


api_router_unversioned = APIRouter()
api_router_unversioned.include_router(health.router, tags=["health_check"])
