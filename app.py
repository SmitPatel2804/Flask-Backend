import os
from flask import Flask
from api.auth import auth_blueprint, init_mongo
from service.unique_key_service import key_blueprint, init_mongo as init_mongo_key  

def create_app():
    """Initialize Flask app and configure MongoDB."""
    app = Flask(__name__)

    # ✅ Use environment variable for Railway, fallback to localhost
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/UserAuth")

    # ✅ Initialize MongoDB once
    if not hasattr(app, "mongo_initialized"):
        init_mongo(app)  
        init_mongo_key(app)  
        app.mongo_initialized = True  

    # ✅ Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix="/api")
    app.register_blueprint(key_blueprint, url_prefix="/api")  

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)
