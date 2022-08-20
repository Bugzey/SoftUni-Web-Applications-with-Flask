from lecture6.resources.auth import RegisterUser, LoginUser
from lecture6.resources.complaint import ComplaintListCreate

routes = (
    (RegisterUser, "/register/"),
    (LoginUser, "/login/"),
    (ComplaintListCreate, "/complainers/complaints"),
)

