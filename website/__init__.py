import imp
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    cors = CORS(app)

    app.config['SECRET_KEY'] = 'BestDevs'

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app
