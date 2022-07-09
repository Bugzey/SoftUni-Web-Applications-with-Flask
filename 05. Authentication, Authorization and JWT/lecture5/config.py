import os

URL = "postgresql://{user}:{password}@{server}:{port}/{database}".format(
    user = os.environ["USER"],
    password = os.environ["PASSWORD"],
    server = os.environ["SERVER"],
    port = os.environ["PORT"],
    database = os.environ["DATABASE"],
)
SECRET = os.environ["SECRET"]

