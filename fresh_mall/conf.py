import secrets
from typing import Optional, Dict, Any, List, Union

from pydantic import BaseSettings, RedisDsn, AnyUrl, validator


class MysqlDsn(AnyUrl):
    allowed_schemes = {'mysql'}
    user_required = True


class RabbitMQDsn(AnyUrl):
    allowed_schemes = {'amqp'}


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # 数据库
    MYSQL_ADDRESS: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    MYSQL_DATABASE_URL: Optional[MysqlDsn] = None

    @validator("MYSQL_DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return MysqlDsn.build(
            scheme="mysql",
            user=values.get("MYSQL_USER"),
            password=values.get("MYSQL_PASSWORD"),
            host=values.get("MYSQL_ADDRESS"),
            path=f"/{values.get('MYSQL_DB', '')}",
        )

    # redis, ip + 端口
    REDIS_ADDRESS: str
    REDIS_URL: Optional[RedisDsn] = None

    @validator("REDIS_URL", pre=True)
    def assemble_redis_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            host=values.get("REDIS_ADDRESS")
        )

    # rabbitMQ
    RABBITMQ_ADDRESS: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_VHOST: str

    RABBITMQ_URL: Optional[RabbitMQDsn] = None

    @validator("RABBITMQ_URL", pre=True)
    def assemble_rabbitmq_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RabbitMQDsn.build(
            scheme="amqp",
            host=values.get("RABBITMQ_ADDRESS"),
            user=values.get("RABBITMQ_USER"),
            password=values.get("RABBITMQ_PASSWORD"),
            path=f'/{values.get("RABBITMQ_VHOST")}'
        )

    # 邮件服务
    EMAIL_USER: str
    EMAIL_SECRET: str
    EMAIL_SMTP_HOST: str = 'smtp.163.com'

    # FastDFS
    TRACKER_ADDRESS: Union[str, Dict[str, Any]]

    @validator("TRACKER_ADDRESS", pre=True)
    def dfs_build_cnf(cls, v: str) -> Dict[str, Any]:
        host, port = v.split(":")
        return {'host_tuple': (host,), 'port': port, 'timeout': 30, 'name': 'Tracker Pool'}

    # 待迁移的 模型类
    APP_MODELS: Optional[List[str]] = ["apps.user.models", "apps.goods.models", "apps.order.models", "aerich.models"]

    class Config:
        case_sensitive = True


settings = Settings(_env_file='.development', _env_file_encoding='utf-8')


# 迁移 aerich init -t fresh_mall.conf.TORTOISE_ORM
TORTOISE_ORM = {
    "connections": {"default": settings.MYSQL_DATABASE_URL},
    "apps": {
        "models": {
            "models": settings.APP_MODELS,
            "default_connection": "default",
        },
    }
}
