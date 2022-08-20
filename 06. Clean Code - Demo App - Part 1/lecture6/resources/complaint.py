from flask import request
from flask_restful import Resource

from lecture6.managers.auth import auth
from lecture6.managers.complaint import ComplaintManager
from lecture6.models import RoleModel

from lecture6.schemas.request.complaint import ComplaintRequestSchema
from lecture6.schemas.response.complaint import ComplaintResponseSchema
from lecture6.utils.decorators import permission_required, validate_schema


class ComplaintListCreate(Resource):
    @auth.login_required
    def get(self):
        user = auth.current_user()
        complaints = ComplaintManager.get_all_complainer_claims(user)
        # Use dump, not load when schema and object are not the same
        return ComplaintResponseSchema().dump(complaints, many=True)


    @auth.login_required
    @permission_required("complainer")
    @validate_schema(ComplaintRequestSchema)
    def post(self):
        complainer = auth.current_user()
        data = request.get_json()
        complaint = ComplaintManager.create(data, complainer.id)
        # Use dump, not load when schema and object are not the same
        return ComplaintResponseSchema().dump(complaint)

