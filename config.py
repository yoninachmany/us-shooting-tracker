import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # TODO: change default SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://localhost/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
