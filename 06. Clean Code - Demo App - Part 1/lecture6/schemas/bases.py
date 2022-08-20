from marshmallow import Schema, fields

class BaseComplaintSchema(Schema):
    title = fields.String(requried = True)
    description = fields.String(required = True)
    photo_url = fields.String(required = True)
    amount = fields.Float(required = True)

