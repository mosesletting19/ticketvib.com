import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'payments.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CONSUMER_KEY = os.getenv("CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
    SHORTCODE = os.getenv("SHORTCODE")
    PASSKEY = os.getenv("PASSKEY")
    CALLBACK_URL = os.getenv("CALLBACK_URL")
    PORT = int(os.getenv("PORT", 5555))
    UPLOAD_FOLDER = 'static/uploads'