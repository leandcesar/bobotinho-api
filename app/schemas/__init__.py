# -*- coding: utf-8 -*-
from app.api import fields
from app.marshmallow import ma


def sort_dict(fields: dict, order: list) -> dict:
    return {key: fields[key] for key in order}


class BaseSchema(ma.Schema):
    class Meta:
        fields = ()

    def as_model(self) -> dict:
        return {
            # flask_marshmallow.fields.fields -> flask_restx.fields
            field: getattr(fields, value.__class__.__name__)(
                description=value.metadata.get("description"),
                required=value.required,
            )
            for field, value in sort_dict(self.fields, order=self.Meta.fields).items()
        }


class BaseSchemaSQL(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ()

    def as_model(self) -> dict:
        return {
            # flask_marshmallow.fields.fields -> flask_restx.fields
            field: getattr(fields, value.__class__.__name__)(
                description=value.metadata.get("description"),
                required=value.required,
                readonly=field in ("id", "created_on", "updated_on") or None,
            )
            for field, value in sort_dict(self.fields, order=self.Meta.fields).items()
        }
