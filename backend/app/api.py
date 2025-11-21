from flask import Blueprint, jsonify, request, current_app

api_bp = Blueprint("api", __name__)


@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@api_bp.route("/sensors/current", methods=["GET"])
def sensors_current():
    app = current_app
    latest = getattr(app, "latest_values", {})
    config = getattr(app, "sensor_config", {})

    sensors = []

    for sensor_id, value in latest.items():
        meta = config.get(sensor_id, {})
        sensors.append(
            {
                "id": sensor_id,
                "name": meta.get("name", sensor_id),
                "value": value,
                "unit": meta.get("unit", ""),
                "group": meta.get("group"),
            }
        )

    return jsonify(sensors)


@api_bp.route("/sensors/<sensor_id>/history", methods=["GET"])
def sensor_history(sensor_id):
    range_param = request.args.get("range", "1h")
    influx = current_app.influx

    points = influx.get_sensor_history(sensor_id, range_param)
    return jsonify(points)
