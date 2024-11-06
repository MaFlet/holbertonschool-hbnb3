import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://hbnb_evo_2:123@localhost/hbnb_evo_2_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}