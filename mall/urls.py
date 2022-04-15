from apps.areas.urls import urlpatterns as ares
from apps.carts.urls import urlpatterns as carts
from apps.goods.urls import urlpatterns as goods
from apps.orders.urls import urlpatterns as orders
from apps.user.urls import urlpatterns as user

urlpatterns = [*user, *ares, *goods, *carts, *orders]
