from __future__ import absolute_import, unicode_literals
"""
首先 从 __future__ 导入absolute_import 进行绝对导入，
这样我们项目下的 celery.py 模块就不会与第三方库 celery 冲突
"""
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
# 然后设置默认 DJANGO_SETTINGS_MODULEcelery 命令行程序的环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gitblogsite.settings')

app = Celery('gitblogsite')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# 将Django设置模块添加为Celery的配置源。
# 这意味着您不必使用多个配置文件，
# 而直接从Django设置中配置Celery。
# 但您也可以根据需要将它们分开。
app.config_from_object('django.conf:settings', namespace='CELERY')

# 大写命名空间意味着所有Celery配置选项必须以大写而不是小写指定，并以开头 CELERY_，
# 例如，task_always_eager设置变为CELERY_TASK_ALWAYS_EAGER，而broker_url 
# 设置变为CELERY_BROKER_URL。



# Load task modules from all registered Django app configs.
# 设置自动发现任务：
#   会从每个已经注册的 app 中的 tasks.py 文件中发现任务
app.autodiscover_tasks()

