from flask import Flask
from api.auth import auth_blueprint, init_mongo
from service.unique_key_service import key_blueprint, init_mongo as init_mongo_key

def create_app():
    """Initialize Flask app and configure MongoDB."""
    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/UserAuth'

    init_mongo(app)  # ✅ Initialize MongoDB in auth.py
    init_mongo_key(app)  # ✅ Initialize MongoDB in unique_key_service.py

    app.register_blueprint(auth_blueprint, url_prefix='/api')
    app.register_blueprint(key_blueprint, url_prefix='/api')

    return app

app = create_app()  # ✅ Ensure `app` is initialized here

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
