from marshmallow import Schema, fields

class UserGetSchema(Schema):
    id = fields.Int(required=True)

class UserPostSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True, load_only = True)

class MessageSchema(Schema):
    msg = fields.String(required=True)

class UserPutSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)