import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('FLASK_DEBUG')
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_LIGHT')
SQLALCHEMY_TRACK_MODIFICATIONS = False
FLASK_ADMIN_SWATCH = 'cosmo'
