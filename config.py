from dotenv import load_dotenv
import os

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = os.environ.get('DEBUG') or False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = ('mysql://{user}:{passw}@{host}/{db}'.format(user=os.environ.get('MYSQL_USER'),
                                                                           passw=os.environ.get('MYSQL_PASS'),
                                                                           host=os.environ.get('MYSQL_HOST'),
                                                                           db=os.environ.get('MYSQL_DB')))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
