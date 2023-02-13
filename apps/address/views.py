from ninja import Path, Query, Router

from apps.address.models import Address
from apps.address.schemas import AddressSchema
from apps.schemas import PageParams, PageResult, R
from apps.views import pagination

# Create your views here.
router = Router(tags=["地址管理"])


@router.post("", summary="添加地址", response=R[AddressSchema])
def create(request, data: AddressSchema):
    if data.is_deault:
        Address.objects.filter(member=request.user, is_default=True).update(
            is_default=False
        )
    address = Address.objects.create(**data.dict(), member=request.user)
    return R.ok(address)


@router.delete("/{id}", summary="删除地址", response=R)
def delete(request, pk: int = Path(..., alias="id")):
    result = Address.objects.filter(id=pk).delete()
    if result[0] == 0:
        return R.fail("数据不存在")
    return R.ok()


@router.get("", summary="查询所有地址", response=R[PageResult[AddressSchema]])
def array(request, page: PageParams = Query(...)):
    data = pagination(page, Address, member=request.user)
    return R.ok(data)


@router.put("/{id}", summary="更新地址", response=R)
def update(request, pk: int = Path(..., alias="id"), *, data: AddressSchema):
    row = Address.objects.filter(member=request.user, id=pk).update(**data.dict())
    if row[0] == 0:
        return R.fail()
    return R.ok()
