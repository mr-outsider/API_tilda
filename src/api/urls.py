from fastapi import APIRouter

from .endpoints import health


api_router_unversioned = APIRouter()
api_router_unversioned.include_router(health.router, tags=["health_check"])
