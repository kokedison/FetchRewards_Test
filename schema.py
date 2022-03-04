from marshmallow import Schema, fields

class TransactionSchema(Schema):
    payer = fields.String(required=True)
    points = fields.Integer(required=True)
    timestamp = fields.DateTime(required=True)

class SpendPointsSchema(Schema):
    points = fields.Integer(required=True)