import os

from flask import Flask


def create_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="static",
    )

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app.config["UPLOAD_FOLDER"] = os.path.join(project_root, "uploads")

    from app.controllers.main_controller import main_bp
    app.register_blueprint(main_bp)

    return app
