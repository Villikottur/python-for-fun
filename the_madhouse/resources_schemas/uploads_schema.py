from marshmallow import Schema, fields, ValidationError


def validate_upload(file: object):
    if not file.filename.endswith(".txt"):
        raise ValidationError


class UploadSchema(Schema):
    file = fields.Field(required=True, validate=validate_upload)
