from marshmallow import Schema, fields

from lecture6.schemas.bases import BaseComplaintSchema

class ComplaintResponseSchema(BaseComplaintSchema):
    id = fields.Integer(required = True)
    status = fields.Integer(required = True)
    created_on = fields.DateTime(required = True)

