from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    from app.extensions import db
    db.init_app(app)
    
    # 初始化JWT
    jwt = JWTManager(app)
    
    # 配置CORS，允许所有来源访问，并处理预检请求
    CORS(app, 
         resources={r"/api/*": {
             "origins": "*",
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"]
         }})
    
    # 注册蓝图
    from app.routes import books, members, borrows, statistics, auth, reviews, reservations
    app.register_blueprint(books.bp, url_prefix='/api')
    app.register_blueprint(members.bp, url_prefix='/api')
    app.register_blueprint(borrows.bp, url_prefix='/api')
    app.register_blueprint(statistics.bp, url_prefix='/api')
    app.register_blueprint(auth.bp, url_prefix='/api')
    app.register_blueprint(reviews.bp, url_prefix='/api')
    app.register_blueprint(reservations.bp, url_prefix='/api')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app