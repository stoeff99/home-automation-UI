from flask import Flask
from .config import Config
from .mqtt_client import init_mqtt
from .influx_client import init_influx
from .loxone_client import LoxoneClient
from .sensors_config import load_sensors_config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Load sensor metadata (for all sensors)
    app.sensor_config = load_sensors_config()

    init_influx(app)
    init_mqtt(app)
    app.loxone = LoxoneClient(
        host=app.config["LOXONE_HOST"],
        username=app.config["LOXONE_USER"],
        password=app.config["LOXONE_PASSWORD"],
    )

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
