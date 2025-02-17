import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///reservations.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '12esperanza12@gmail.com'
    MAIL_PASSWORD = 'nisd vmzu yewi cuma'  # 生成されたアプリパスワードを使用
    MAIL_DEFAULT_SENDER = '12esperanza12@gmail.com'
