from flask import abort, request
from functools import wraps
import re

from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    ValidationError,
)

def validate_schema(schema: Schema):
    def decorator(fun):
        @wraps(fun)
        def decorated_function(*args, **kwargs):
            data = request.json
            item = schema()
            errors = item.validate(data)
            if errors:
                abort(400, errors)

            return fun(*args, **kwargs)

        return decorated_function

    return decorator


class UserBaseSchema(Schema):
    username = fields.String(required = True)
    email = fields.Email(required = True)
    first_name = fields.String()
    last_name = fields.String()

class UserSignUpSchema(UserBaseSchema):
    password = fields.String(required = True)

    @validates("password")
    def validate_password(self, password: str) -> None:
        checks = (
            (lambda x: re.search("[a-zA-Z]", x) is None, "Password needs at least one letter"),
            (lambda x: re.search("\d", x) is None, "Password needs at least one number"),
            (lambda x: re.search("\W", x) is None, "Password needs at least one non-number and non-letter item"),
        )

        for test, error in checks:
            if test(password):
                raise ValidationError(error)

