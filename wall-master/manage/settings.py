"""
    :配置项文件
    :以键值对的形式表示
"""

import os
from manage import app

dev_db = 'sqlite:///' + os.path.join(os.path.dirname(app.root_path),'data.db')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不追踪对象的修改
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db) 