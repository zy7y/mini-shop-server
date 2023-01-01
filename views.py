from typing import Type

from apps.models import MallBaseModel
from apps.schemas import PageParams


def pagination(page: PageParams, model: Type[MallBaseModel], **kwargs):
    start = (page.offset - 1) * page.limit
    end = start + page.limit
    queryset = model.objects.filter(**kwargs)
    items = [query.__dict__ for query in queryset[start: end]]
    return dict(count=queryset.count(), items=items)