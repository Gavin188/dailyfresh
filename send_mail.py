import os
import time

from celery import Celery, shared_task
from django.conf import settings

# 创建一个Celery类的实例对象   redis 作为消息中间件
from django.core.mail import send_mail

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()
app = Celery('send_mail', broker='redis://127.0.0.1:6379/8')


# 定义任务函数
@app.task(name='send_mail')
def send_register_active_email(to_email, username):
    print('发送中=----')
    print('发送中=----', to_email)
    print('发送中=----', username)
    '''发送激活邮件'''
    # 组织邮件信息
    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/>' \
                   '<a href="http://127.0.0.1:8083/user/active">http://127.0.0.1:8083/user/active</a>' % (
                       username)

    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)
    # print('')
    return '发送成功'


@app.task(name='add')
def add(x, y):
    return '你的姓名是' + x + ',年龄：' + y


@shared_task(name='tell')
def tell():
    print(12111)
    x = '余帅'
    y = '30'
    return '你的姓名是' + x + ',年龄：' + y


if __name__ == '__main__':
    email = 'Gavin Z.H. Guo/CEN/FOXCONN'
    name = '余帅'
    # token1 = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MTEwMTY4MywiZXhwIjoxNTcxMTA1MjgzfQ.eyJjb25maXJtIjozf' \
    #          'Q.AbV3FD6VoXhbtNTbsGIvq0bQfeTP22Zw9N1VOpdvsNDa5DYBe6cv6qVT3elSt8p6lV9u-zpahHyj98Y8sgL75A'

    # send_register_active_email.delay(email, name)
    # result = add.delay('余帅', '30')
    # print(result)

    tell.delay()
