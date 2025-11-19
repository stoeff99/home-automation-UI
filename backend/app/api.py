from flask import Blueprint, jsonify, request, current_app

api_bp = Blueprint("api", __name__)


@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@api_bp.route("/sensors/current", methods=["GET"])
def sensors_current():
    """
    Returns latest sensor values.
    For now: combine dummy Loxone data plus last known MQTT/Influx values if desired.
    Here we just return a static list as a minimal working example.
    """
    data = [
        {"id": "temp_living", "name": "Living Room Temp", "value": 22.5, "unit": "°C"},
        {"id": "humidity_living", "name": "Living Room Humidity", "value": 45, "unit": "%"},
    ]
    return jsonify(data)


@api_bp.route("/sensors/<sensor_id>/history", methods=["GET"])
def sensor_history(sensor_id):
    """
    Return historical data from InfluxDB.
    Query params: ?range=1h / 24h / 7d etc.
    """
    range_param = request.args.get("range", "1h")
    influx = current_app.influx

    points = influx.get_sensor_history(sensor_id, range_param)
    return jsonify(points)


@api_bp.route("/actuators/<actuator_id>", methods=["POST"])
def set_actuator(actuator_id):
    """
    Send command to an actuator via MQTT.
    Body: { "value": ... }
    """
    payload = request.json or {}
    value = payload.get("value")
    if value is None:
        return jsonify({"error": "Missing 'value'"}), 400

    mqtt_client = current_app.mqtt_client
    topic = f"home/actuators/{actuator_id}/set"
    mqtt_client.publish(topic, str(value))

    return jsonify({"status": "sent", "actuator": actuator_id, "value": value})
