import os
from celery import Celery

# Django 설정 모듈 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upbit_project.settings')

# Celery 앱 생성
app = Celery('upbit_project')

# Celery 설정 로드
app.config_from_object('django.conf:settings', namespace='CELERY')

# 태스크 모듈 자동으로 찾기
app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True