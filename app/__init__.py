from flask import Flask


def create_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="static",
    )

    from app.controllers.main_controller import main_bp
    app.register_blueprint(main_bp)

    return app
