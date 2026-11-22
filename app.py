"""ApexRide Nepal — Luxury Vehicle Rental Platform (Flask + SQLite).
Run:  pip install -r requirements.txt
       python app.py
Then open http://127.0.0.1:5000
"""
import os
from flask import Flask, render_template
from models import db
from seed import seed

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "apexride-nepal-secret-key-change-in-production")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "apexride.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB (walkaround videos)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)

    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.vehicles import veh_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(veh_bp)

    @app.context_processor
    def inject_user():
        from flask import session
        return dict(session_user_name=session.get("user_name"),
                    session_user_role=session.get("user_role"))

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500

    with app.app_context():
        db.create_all()
        seed()
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
