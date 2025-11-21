# backend/app/influx_client.py

import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxClient:
    def __init__(self, url, token, org, bucket):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket

        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def write_sensor_value(self, sensor_id: str, value: float):
        point = (
            Point("sensor")
            .tag("id", sensor_id)
            .field("value", float(value))
        )
        self.write_api.write(bucket=self.bucket, org=self.org, record=point)

    def get_sensor_history(self, sensor_id: str, range_param: str = "1h"):
        """
        Return list of {time: ISO8601, value: float} for the given sensor_id.
        range_param like "1h", "6h", "24h", "7d" etc.
        """
        # Simple safety: default to 1h if weird input
        if not range_param:
            range_param = "1h"

        flux = f"""
        from(bucket: "{self.bucket}")
          |> range(start: -{range_param})
          |> filter(fn: (r) => r._measurement == "sensor")
          |> filter(fn: (r) => r.id == "{sensor_id}")
          |> filter(fn: (r) => r._field == "value")
          |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)
          |> yield(name: "mean")
        """

        tables = self.query_api.query(flux)
        points = []

        for table in tables:
            for record in table.records:
                points.append(
                    {
                        "time": record.get_time().isoformat(),
                        "value": record.get_value(),
                    }
                )

        return points


def init_influx(app):
    url = app.config["INFLUX_URL"]
    token = app.config["INFLUX_TOKEN"]
    org = app.config["INFLUX_ORG"]
    bucket = app.config["INFLUX_BUCKET"]

    app.influx = InfluxClient(url, token, org, bucket)
