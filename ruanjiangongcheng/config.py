import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'string2333'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = basedir + "/uploads/"
    ALLOWED_EXTENSIONS = ("rar", "zip")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:%s/%s" % \
                              ('root', 'yourpassword', '127.0.0.1', '3306', 'yourDBname')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:%s/%s" % \
                              ('root', 'yourpassword', '127.0.0.1', '3306', 'yourDBname')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:%s/%s" % \
                              ('root', 'yourpassword', '127.0.0.1', '3306', 'yourDBname')


WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
