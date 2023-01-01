from ninja import NinjaAPI

from apps.auth import AuthBearer
from apps.exceptions import handle_exceptions

api = NinjaAPI(title="Django mall", csrf=True)

handle_exceptions(api)

from apps.member.views import router

api.add_router("/member", router)

from apps.address.views import router
api.add_router("/address", router, auth=AuthBearer())
