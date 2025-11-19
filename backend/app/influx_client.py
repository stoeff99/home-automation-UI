from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxWrapper:
    def __init__(self, url, token, org, bucket):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.org = org
        self.bucket = bucket
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def write_sensor_value(self, sensor_id, value):
        try:
            value = float(value)
        except ValueError:
            return

        p = (
            Point("sensor")
            .tag("id", sensor_id)
            .field("value", value)
        )
        self.write_api.write(bucket=self.bucket, org=self.org, record=p)

    def get_sensor_history(self, sensor_id, range_str="1h"):
        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: -{range_str})
          |> filter(fn: (r) => r["_measurement"] == "sensor")
          |> filter(fn: (r) => r["id"] == "{sensor_id}")
          |> filter(fn: (r) => r["_field"] == "value")
          |> keep(columns: ["_time", "_value"])
          |> sort(columns: ["_time"])
        '''
        tables = self.query_api.query(query=query, org=self.org)

        result = []
        for table in tables:
            for record in table.records:
                result.append(
                    {
                        "time": record.get_time().isoformat(),
                        "value": record.get_value(),
                    }
                )
        return result


def init_influx(app):
    app.influx = InfluxWrapper(
        url=app.config["INFLUX_URL"],
        token=app.config["INFLUX_TOKEN"],
        org=app.config["INFLUX_ORG"],
        bucket=app.config["INFLUX_BUCKET"],
    )
