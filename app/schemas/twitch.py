# -*- coding: utf-8 -*-
from app.marshmallow import fields
from app.schemas import BaseSchema


class TwitchSchema(BaseSchema):
    class Meta:
        fields = (
            "id",
            "avatar",
            "follows",
            "total_views",
            "title",
            "game",
            "uptime",
            "viewers",
            "account_age",
            "creation",
            "follow_age",
            "followed",
        )

    id = fields.Integer(allow_none=True, description="Twitch channel ID")
    avatar = fields.String(allow_none=True, description="URL of the avatar for the channel")
    follows = fields.Integer(allow_none=True, description="Amount of followers a channel has")
    total_views = fields.Integer(allow_none=True, description="Total views a channel has")
    title = fields.String(allow_none=True, description="Current title set on the channel")
    game = fields.String(allow_none=True, description="Current game the channel has been set to")
    uptime = fields.String(allow_none=True, description="How long the channel has been live for the current streaming")
    viewers = fields.String(allow_none=True, description="How many viewers the channel has, if they are currently streaming")
    account_age = fields.String(allow_none=True, description="Date and time difference between when channel created account and now")
    creation = fields.String(allow_none=True, description="Creation date and time of the channel")
    follow_age = fields.String(allow_none=True, description="Date and time difference between when user followed channel")
    followed = fields.String(allow_none=True, description="Date and time of when user followed channel")
