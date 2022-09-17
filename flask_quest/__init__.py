import os
import config
from flask import Flask
from flask_bootstrap import Bootstrap

# создание экземпляра приложения
app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')
bootstrap = Bootstrap(app)
'''
Если переменная среды FLASK_ENV не задана, 
приложение запустится в режиме отладки 
(то есть, app.debug = True). 
Чтобы перевести приложение в рабочий режим, 
нужно установить для переменной среды FLASK_ENV 
значение config.ProductionConfig.
'''
from . import views
