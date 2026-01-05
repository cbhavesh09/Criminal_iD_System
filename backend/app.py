from flask import Flask, jsonify
from flask_cors import CORS

from config import Config, db
from routes.auth_routes import auth_bp
from routes.criminal_routes import criminal_bp
from routes.identify_routes import identify_bp


def create_app():
    app = Flask(__name__)

    # ==============================
    # CONFIG
    # ==============================
    app.config["SECRET_KEY"] = Config.SECRET_KEY
    app.config["ENV"] = Config.FLASK_ENV
    app.config["DEBUG"] = Config.FLASK_DEBUG

    # ==============================
    # CORS (PRODUCTION READY)
    # ==============================
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5500",
                "http://127.0.0.1:5500",
                "https://criminal-i-d-system.vercel.app"
            ]
        },
        r"/auth/*": {
            "origins": [
                "http://localhost:5500",
                "http://127.0.0.1:5500",
                "https://criminal-i-d-system.vercel.app"
            ]
        }
    },
    supports_credentials=True
)


    # ==============================
    # ROUTES
    # ==============================
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "Criminal Identification System API running",
            "status": "OK"
        })

    @app.route("/health", methods=["GET"])
    def health():
        try:
            db.command("ping")
            return jsonify({
                "status": "healthy",
                "database": "connected"
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "database": "disconnected",
                "error": str(e)
            }), 500

    # ==============================
    # BLUEPRINTS
    # ==============================
    app.register_blueprint(auth_bp)
    app.register_blueprint(criminal_bp)
    app.register_blueprint(identify_bp)

    return app


# ==============================
# GUNICORN ENTRYPOINT
# ==============================
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
