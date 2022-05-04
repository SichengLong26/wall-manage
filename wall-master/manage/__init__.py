"""
    :构造文件（每个包的__init__.py文件）：包含程序实例
    :该文件用于放包的初始化代码，也可以为空
    :当包或者包内的模块被导入时，构造文件将被自动执行
"""
from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

app = Flask('manage')  # Flask通过传入的参数__name__来确定程序路径
app.jinja_env.trim_blocks = True  # 删除jinja2语句的后一个空行
app.jinja_env.lstrip_blocks = True  # 删除jinja2语句行之前的空格和制表符
app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)
bootstrap = Bootstrap4(app)
moment = Moment(app)

from manage import models, views, commands