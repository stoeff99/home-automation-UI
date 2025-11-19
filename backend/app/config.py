import os


class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    # Loxone
    LOXONE_HOST = os.getenv("LOXONE_HOST", "loxone")
    LOXONE_USER = os.getenv("LOXONE_USER", "user")
    LOXONE_PASSWORD = os.getenv("LOXONE_PASSWORD", "password")

    # MQTT
    MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "mosquitto")
    MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))

    # InfluxDB
    INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
    INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "my-token")
    INFLUX_ORG = os.getenv("INFLUX_ORG", "home")
    INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "sensors")
