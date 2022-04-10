from typing import Dict

from fdfs_client.client import Fdfs_client
from aioredis import from_url, Redis

from .conf import settings

# FastDFS 客户端
FastDFSManager = Fdfs_client(settings.TRACKER_ADDRESS)

# Redis 客户端
RedisManager: Dict[int, Redis] = {
    db: from_url(settings.REDIS_URL, db=db, max_connections=10, encoding="utf-8",
                 decode_responses=True)
    for db in range(16)
}

# 验证码使用的 redis库
img_code_redis = RedisManager.get(0)
sms_code_redis = RedisManager.get(1)

