"""router插件
根据 typehint 绑定responseModel
实现参考 https://github.com/tiangolo/fastapi/issues/620
"""

from typing import Any, Callable, get_type_hints

from fastapi.routing import APIRoute


class Route(APIRoute):
    def __init__(self, path: str, endpoint: Callable[..., Any], **kwargs: Any):
        if kwargs.get("response_model") is None:
            kwargs["response_model"] = get_type_hints(endpoint).get("return")
        super(Route, self).__init__(path=path, endpoint=endpoint, **kwargs)
