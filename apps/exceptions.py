from ninja import NinjaAPI
from django.db.utils import DatabaseError
from jwt.exceptions import PyJWTError

from apps.schemas import R


def handle_exceptions(app: NinjaAPI):

    def handler(request, exc):
        return app.create_response(
            request,
            R.fail(str(exc)),
            status=200,
        )

    app.add_exception_handler(DatabaseError, handler=handler)

    app.add_exception_handler(PyJWTError, handler=handler)

    app.add_exception_handler(ValueError, handler=handler)
