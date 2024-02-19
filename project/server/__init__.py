import os

from flask import Flask
from flask_restful import Api



def create_app(script_info=None):

    # instantiate the app
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static",
    )

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # Captura todos los errores 404
    api = Api(app, catch_all_404s=True)
    
    # Deshabilita el modo estricto de acabado de una URL con /
    app.url_map.strict_slashes = False
    
    # register blueprints
    from project.server.main import main_blueprint

    app.register_blueprint(main_blueprint)

    # shell context for flask cli
    app.shell_context_processor({"app": app})

    return app
