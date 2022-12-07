from linkzone.common.exceptions import UserValueError
from linkzone.core.requests_interface import RequestsInterface


class Authentication(RequestsInterface):
    """
    Class for authentication requests
    """

    def __init__(self) -> None:
        super().__init__()
        self._token: str | None = None
        self._requests_body_auth = self.requests_body["Authentication"]

    def login(self, password: str) -> dict:
        """Login method
        :params password: Password for login
        :returns: Token when login is correct and error when is not
        """
        if password == "":
            raise UserValueError("A not empty string must be provided as a password")
        self._requests_body_auth["Login"]["params"]["Password"] = password
        response = self.post(data=self._requests_body_auth["Login"])
        if "error" in response.keys():
            return response["error"]["message"]
        else:
            self._token = response["result"]["token"]
            return self._token
