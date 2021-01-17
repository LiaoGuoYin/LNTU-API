import base64

from celery import Celery

from appPush.push import apple_push

celery = Celery('appPush.tasks', broker='redis://127.0.0.1:6379', backend='redis://127.0.0.1:6379')


@celery.task
def push_notice(content: str, token_list: [str]):
    print('开始推送通知任务')
    decrypted_token_list = [base64.b64decode(each).hex() for each in token_list]  # exception handler
    apple_push(content=content, device_token_list=decrypted_token_list)
