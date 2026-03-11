import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or os.getenv('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')