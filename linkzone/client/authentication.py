from linkzone.common.exceptions import UserValueError
from linkzone.core.requests_interface import RequestsInterface


class Authentication(RequestsInterface): 
    def __init__(self) -> None:
        super().__init__()
        self._token: str | None = None

    def login(self, password: str) -> str:
        """ Login method
        :params password: Password for login
        :returns: Token when login is correct and error when is not
        """
        if password == "":
            raise UserValueError("A not empty string must be provided as a password")
        self.requests_body["Authentication"]["Login"]["params"]["Password"] = password
        response = self.post(data=self.requests_body["Authentication"]["Login"])
        if "error" in response.keys():
            return response["error"]["message"]
        else:
            self._token = self.post(data=self.requests_body["Authentication"]["Login"])[
                "result"
            ]["token"]
            return self._token
