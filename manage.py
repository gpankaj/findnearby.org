from flask.ext.script import Manager
from app import create_app
import os

my_app_obj = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(my_app_obj)



if __name__ == '__main__':
    manager.run()
