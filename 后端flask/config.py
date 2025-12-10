import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "library.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 应用配置
    DEBUG = True
    TESTING = False
    
    # CORS配置
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
    
    # 上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # 会话配置
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}