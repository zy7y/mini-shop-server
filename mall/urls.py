from apps.areas.urls import urlpatterns as ares
from apps.goods.urls import urlpatterns as goods
from apps.user.urls import urlpatterns as user

urlpatterns = [*user, *ares, *goods]
