from functools import wraps

from flask import request

from lecture6.db import sess
from lecture6.models import RoleModel
from lecture6.managers.auth import auth

def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            schema = schema_name()
            errors = schema.validate(request.get_json())
            if errors:
                return f"Invalid fields {errors}", 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def permission_required(role: str):
    def decorator(fun):
        @wraps(fun)
        def decorated(*args, **kwargs):
            role_id = sess \
                .query(RoleModel.id) \
                .where(RoleModel.role == role) \
                .scalar()
            current_user = auth.current_user()
            if current_user.role_id != role_id:
                return "Insufficient priviledges", 403

            return fun(*args, **kwargs)
        return decorated
    return decorator

