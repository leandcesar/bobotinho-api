# -*- coding: utf-8 -*-
from app.marshmallow import fields
from app.schemas import BaseSchema


class WeatherSchema(BaseSchema):
    class Meta:
        fields = (
            "id",
            "name",
            "country",
            "lon",
            "lat",
            "temp",
            "temp_feels_like",
            "temp_min",
            "temp_max",
            "visibility",
            "speed",
            "deg",
            "clouds",
            "pressure",
            "humidity",
            "description",
            "emoji",
        )

    id = fields.Integer(allow_none=True, description="City ID")
    name = fields.String(allow_none=True, description="City name")
    country = fields.String(allow_none=True, description="Country code")
    lon = fields.Float(allow_none=True, description="City geo location, longitude")
    lat = fields.Float(allow_none=True, description="City geo location, latitude")
    temp = fields.Float(description="Current temperature")
    temp_feels_like = fields.Float(allow_none=True, description="Temperature parameter accounts for the human perception of weather")
    temp_min = fields.Float(allow_none=True, description="Minimum temperature at the moment")
    temp_max = fields.Float(allow_none=True, description="Maximum temperature at the moment")
    speed = fields.Float(allow_none=True, description="Wind speed")
    deg = fields.Float(allow_none=True, description="Wind direction")
    clouds = fields.Float(allow_none=True, description="Percentage of cloudiness")
    humidity = fields.Float(allow_none=True, description="Percentage of humidity")
    visibility = fields.Integer(allow_none=True, description="Visibility")
    pressure = fields.Float(allow_none=True, description="Atmospheric pressure")
    description = fields.String(allow_none=True, description="Weather condition within the group")
    emoji = fields.String(allow_none=True, description="Weather emoji")
