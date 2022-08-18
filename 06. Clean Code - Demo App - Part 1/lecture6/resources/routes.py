from lecture6.resources.auth import RegisterUser, LoginUser

routes = (
    (RegisterUser, "/register/"),
    (LoginUser, "/login/"),
)

