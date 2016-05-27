from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from config import config
import os



bootstrap_obj = Bootstrap()
login_manager = LoginManager()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['WTF_CSRF_CHECK_DEFAULT'] = 'False'

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)


    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/livedeals'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 't0p s3r3t'


    #Initilize all the flask object with app
    bootstrap_obj.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = "strong"

    print "app created"


    from service_provider import service_provider as service_provider_blueprint
    app.register_blueprint(service_provider_blueprint)



    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


    return app