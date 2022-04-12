from celery import Celery

from mall.conf import settings

celery_app = Celery("worker", broker=settings.RABBITMQ_URL)

# 自动注册异步任务
celery_app.autodiscover_tasks(["celery_tasks"])


#  celery -A celery_tasks.main worker -l info


# windows
# pip install eventlet
# celery -A celery_tasks.main worker -l info -P eventlet
