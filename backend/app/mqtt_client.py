import threading
import paho.mqtt.client as mqtt
import ssl


# In-memory latest values: sensor_id -> float
latest_values = {}


# Map topic prefixes to internal sensor IDs
TOPIC_PREFIX_MAP = {
    "modbus/0/inputRegisters/30529 PVGesamtertrag": "pv_total_yield",
    "modbus/0/inputRegisters/30535 PVTagesertrag": "pv_daily_yield",
    "modbus/0/inputRegisters/30775 PVLeistung": "pv_power",

    "/tempc": "temp_outside",
    "/humidity": "humidity_outside",
    "/windgustkmh": "wind_gust_kmh",
    "/solarradiation": "solar_radiation",

    "venus-home/N/c0619ab7a15e/pvinverter/20/Ac/Power": "venus_pv_power",
    "venus-home/N/c0619ab7a15e/grid/30/Ac/Power": "venus_grid_power",
    "venus-home/N/c0619ab7a15e/vebus/276/Ac/ActiveIn/P": "venus_ac_in_power",
    "venus-home/N/c0619ab7a15e/vebus/276/Dc/0/Power": "venus_dc_power",
    "venus-home/N/c0619ab7a15e/system/0/Dc/Battery/Soc": "venus_battery_soc",
    "venus-home/N/c0619ab7a15e/pvinverter/20/Ac/Energy/Forward": "venus_pv_energy_forward",

    "Weather/calc__48_ttmean": "weather_mean_temp",
    "Weather/cur_sr": "weather_solar_radiation",
    "ecowitt/0C8B95D5E0C7": "ecowitt_station",
    "s4l/mqttlive/1/Aktuelle_Produktion_in_kW/Default": "pv_production_s4", 
}


# Subscriptions matching all your sensors
SUBSCRIPTIONS = [
    "home/sensors/#",

    "modbus/0/inputRegisters/30529 PVGesamtertrag/#",
    "modbus/0/inputRegisters/30535 PVTagesertrag/#",
    "modbus/0/inputRegisters/30775 PVLeistung/#",

    "/tempc/#",
    "/humidity/#",
    "/windgustkmh/#",
    "/solarradiation/#",

    "venus-home/N/c0619ab7a15e/pvinverter/20/Ac/Power/#",
    "venus-home/N/c0619ab7a15e/grid/30/Ac/Power/#",
    "venus-home/N/c0619ab7a15e/vebus/276/Ac/ActiveIn/P/#",
    "venus-home/N/c0619ab7a15e/vebus/276/Dc/0/Power/#",
    "venus-home/N/c0619ab7a15e/system/0/Dc/Battery/Soc/#",
    "venus-home/N/c0619ab7a15e/pvinverter/20/Ac/Energy/Forward/#",

    "Weather/calc__48_ttmean/#",
    "Weather/cur_sr/#",
    "ecowitt/0C8B95D5E0C7/#",
    "s4l/mqttlive/1/Aktuelle_Produktion_in_kW/Default/#",
]


# -----------------------------
# MQTT CALLBACKS
# -----------------------------

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected to MQTT with result code", rc)

    # rc = 0 means success
    if rc != 0:
        print("⚠️  MQTT connection FAILED. Return code:", rc)
        if rc == 4:
            print("❌ Bad username or password.")
        elif rc == 5:
            print("❌ Not authorized — credentials invalid OR ACL blocked.")
        return

    # Subscribe to topics
    for sub in SUBSCRIPTIONS:
        print(f"Subscribing to {sub}")
        client.subscribe(sub)


def resolve_sensor_id(topic: str) -> str | None:
    """Resolve MQTT topic to our internal sensor_id."""
    if topic.startswith("home/sensors/"):
        return topic[len("home/sensors/") :]

    for prefix, sensor_id in TOPIC_PREFIX_MAP.items():
        if topic.startswith(prefix):
            return sensor_id

    return None


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"MQTT message: {topic} -> {payload}")

    app = userdata["flask_app"]
    influx = app.influx

    sensor_id = resolve_sensor_id(topic)
    if not sensor_id:
        return

    try:
        value = float(payload)
    except ValueError:
        print("Invalid numeric value from MQTT:", payload)
        return

    latest_values[sensor_id] = value

    if not hasattr(app, "latest_values"):
        app.latest_values = {}
    app.latest_values[sensor_id] = value

    try:
        influx.write_sensor_value(sensor_id, value)
    except Exception as e:
        print("Error writing to InfluxDB:", e)


# -----------------------------
# MQTT INITIALIZER
# -----------------------------

def init_mqtt(app):
    broker_host = app.config["MQTT_BROKER_HOST"]
    broker_port = app.config["MQTT_BROKER_PORT"]

    username = app.config.get("MQTT_USERNAME")
    password = app.config.get("MQTT_PASSWORD")

    tls_enabled = str(app.config.get("MQTT_TLS_ENABLED", "false")).lower() == "true"
    tls_ca_cert = app.config.get("MQTT_TLS_CA_CERT")

    client = mqtt.Client(client_id="flask-backend", userdata={"flask_app": app})

    # Username/password auth
    if username:
        print(f"Using MQTT credentials: username={username}")
        client.username_pw_set(username, password)

    # TLS
    if tls_enabled:
        print("Enabling MQTT TLS...")
        if tls_ca_cert:
            client.tls_set(tls_ca_cert, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
        else:
            client.tls_set()  # Use system CA
        client.tls_insecure_set(False)

    client.on_connect = on_connect
    client.on_message = on_message

    def run():
        print(f"Connecting to MQTT broker {broker_host}:{broker_port}...")
        try:
            client.connect(broker_host, broker_port, 60)
            client.loop_forever()
        except Exception as e:
            print("❌ MQTT connection error:", e)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    app.mqtt_client = client
