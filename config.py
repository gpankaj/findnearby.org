__author__ = 'pankajg'
import os


class Auth:
    """Google Project Credentials"""
    1073719846868 - 502
    CLIENT_ID = ('563959952938-r23rkq28rs5mm3netmk9di3ne8kpr3f8.apps.googleusercontent.com')
    CLIENT_SECRET = 'KLn0sUmsXUkEfviIUsabmaAr'
    REDIRECT_URI = 'http://localhost:5000/gCallback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    OAUTHLIB_INSECURE_TRANSPORT = '1'
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_ENABLED = False
    SCOPE = ['profile', 'email']

class Config:
    #UPLOAD_FOLDER = 'c:\myapp\\'
    UPLOAD_FOLDER = 'C:\Users\pankajg\Desktop\flask\livedeals\static\images\\'

    SECRET_KEY = os.environ.get('SECRET_KEY')
    WTF_CSRF_CHECK_DEFAULT =False
    WTF_CSRF_ENABLED = False

class DevelopmentConfig(Config):
    DEBUG=True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3r3t'


class TestingConfig(Config):
    TESTING=True

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}