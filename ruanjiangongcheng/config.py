import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'string2333'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:%s/%s" % \
                              ('root', '1234', '127.0.0.1', '3306', 'ruanjiangongcheng')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:%s/%s" % \
                              ('root', '1234', '127.0.0.1', '3306', 'ruanjiangongcheng')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:%s/%s" % \
                              ('root', '1234', '127.0.0.1', '3306', 'ruanjiangongcheng')


WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
