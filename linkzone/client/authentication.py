from linkzone.common.exceptions import UserValueError
from linkzone.core.requests_interface import RequestsInterface


class Authentication(RequestsInterface):
    def __init__(self, password: str) -> None:
        super().__init__()
        if password == "":
            raise UserValueError("A not empty string must be provided as a password")
        self.password = password
        self._token: str | None = None

    def login(self):
        self.requests_body["Authentication"]["Login"]["params"][
            "Password"
        ] = self.password
        self._token = self.post(data=self.requests_body["Authentication"]["Login"])[
            "result"
        ]["token"]
        return self._token
