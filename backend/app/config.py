import os


class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    # Loxone
    LOXONE_HOST = os.getenv("LOXONE_HOST", "192.168.20.2")
    LOXONE_USER = os.getenv("LOXONE_USER", "HA")
    LOXONE_PASSWORD = os.getenv("LOXONE_PASSWORD", "%Daniela2025")

    # MQTT
    MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "192.168.20.4")
    MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    MQTT_USERNAME = os.getenv("MQTT_USERNAME")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
    MQTT_TLS_ENABLED = os.getenv("MQTT_TLS_ENABLED", "false").lower() == "true"
    MQTT_TLS_CA_CERT = os.getenv("MQTT_TLS_CA_CERT")

    # InfluxDB
    INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
    INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "my-token")
    INFLUX_ORG = os.getenv("INFLUX_ORG", "home")
    INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "sensors")

