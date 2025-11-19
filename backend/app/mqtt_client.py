import threading
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected to MQTT with result code", rc)
    client.subscribe("home/sensors/#")


def on_message(client, userdata, msg):
    from flask import current_app

    topic = msg.topic
    payload = msg.payload.decode()
    print(f"MQTT message: {topic} -> {payload}")

    try:
        _, _, sensor_id = topic.split("/", 2)  # home/sensors/<sensor_id>
    except ValueError:
        return

    app = userdata["flask_app"]
    influx = app.influx

    try:
        influx.write_sensor_value(sensor_id, payload)
    except Exception as e:
        print("Error writing to InfluxDB:", e)


def init_mqtt(app):
    broker_host = app.config["MQTT_BROKER_HOST"]
    broker_port = app.config["MQTT_BROKER_PORT"]

    client = mqtt.Client(client_id="flask-backend", userdata={"flask_app": app})
    client.on_connect = on_connect
    client.on_message = on_message

    def run():
        client.connect(broker_host, broker_port, 60)
        client.loop_forever()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    app.mqtt_client = client
