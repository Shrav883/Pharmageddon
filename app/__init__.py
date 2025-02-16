# from flask import Flask
# from config import Config  # Import Config class if you have one
# from flask_pymongo import PyMongo
#
# mongo = PyMongo()
#
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
#
#     mongo.init_app(app)
#
#     # Import blueprints and register them if needed
#     from app.routes import main_bp
#     app.register_blueprint(main_bp)
#
#     return app
from flask import Flask
from config import Config
from flask_pymongo import PyMongo

mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)

    from app.routes import main_bp  # ✅ Import Blueprint
    app.register_blueprint(main_bp)  # ✅ Register it

    return app
