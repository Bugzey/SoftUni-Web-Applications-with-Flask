from lecture6.db import sess
from lecture6.models import (
    ComplaintModel, UserModel, RoleModel, StatusModel,
)

class ComplaintManager:
    @staticmethod
    def get_all_complainer_claims(user: UserModel):
        role_id = sess.query(RoleModel) \
            .where(RoleModel.role == "complainer") \
            .scalar()
        if user.role_id == role_id:
            return ComplaintModel.query.filter_by(complainer_id=user.id).all()
        return sess.query(ComplaintModel).all()

    @staticmethod
    def create(data, complainer_id):
        data["complainer_id"] = complainer_id

        complaint = ComplaintModel(**data)
        if complaint.status_id is None:
            complaint.status_id = sess. \
                query(StatusModel.id) \
                .where(StatusModel.status == "pending") \
                .scalar()

        sess.add(complaint)
        sess.expunge(complaint) # yuck:
        #https://stackoverflow.com/questions/8253978/sqlalchemy-get-object-not-bound-to-a-session
        return complaint
