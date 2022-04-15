from elasticsearch import AsyncElasticsearch

from apps.goods.models import SKU, SPU, GoodsCategory
from mall.conf import settings

client = AsyncElasticsearch(hosts=settings.ELASTICSEARCH_ADDRESS)
index = "mall"


async def to_es():
    """数据库数据插入Es"""
    results = await SKU.filter(is_delete=False, is_launched=True).order_by("-id").all()
    for result in results:
        await client.index(
            index,
            body={
                **result.__dict__,
                "category": await GoodsCategory.filter(pk=result.category_id).values(
                    "id", "name"
                ),
                "spu": await SPU.filter(pk=result.spu_id).values(),
            },
        )


async def query_es(query: str, page: int, page_size: int):
    """查询"""
    body = {
        "from": page_size / page,
        "size": page_size,
        "query": {"multi_match": {"query": query, "fields": ["*", "_source"]}},
    }
    response = await client.search(index=index, body=body)
    total = response["hits"]["total"]["value"]

    return total, [hit["_source"] for hit in response["hits"]["hits"]]
