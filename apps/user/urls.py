from fastapi.routing import APIRoute

from .views import register

urlpatterns = [
    APIRoute("/register", register, methods=["POST"])
]