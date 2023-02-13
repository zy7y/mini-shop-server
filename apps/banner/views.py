from typing import List

from ninja import Router

from apps.banner.models import Banner
from apps.banner.schemas import BannerSchema
from apps.schemas import R

router = Router(tags=["轮播图"])


@router.get("", summary="轮播图列表", response=R[List[BannerSchema]])
def array(request):
    data = Banner.objects.filter(hidden=False).order_by('-sort')
    return R.ok([i.__dict__ for i in data])
