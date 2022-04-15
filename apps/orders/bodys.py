from mall.bodys import BaseBody


class OrderBody(BaseBody):
    address_id: int
    pay_method: int
