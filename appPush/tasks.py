from celery import Celery

from app.schemas import NotificationSubscriptionEnum
from appPush.push import apple_push

celery = Celery('appPush.tasks', broker='redis://127.0.0.1:6379', backend='redis://127.0.0.1:6379')


@celery.task
def push_notice(body: str, device_token_list: [str]):
    print('教务在线发新通知啦!')
    apple_push(NotificationSubscriptionEnum.NOTICE.value, title='教务在线发新通知啦!', body=body,
               device_token_list=device_token_list)
