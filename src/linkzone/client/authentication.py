from typing import Dict
from linkzone.common.exceptions import UserValueError
from linkzone.common.data_models import LoginRequest, LoginParams
from linkzone.core.base_api_client import BaseAPIClient


class Authentication(BaseAPIClient[Dict[str, str]]):  # Especificar tipo de respuesta
    """
    Class for authentication requests
    """

    ERROR_MSG_PASSWORD_REQUIRED = "A not empty string must be provided as a password"

    def __init__(self) -> None:
        super().__init__()
        self._token: str | None = None
        self._login_request: LoginRequest = LoginRequest(params=LoginParams())

    def login(self, password: str) -> Dict[str, any]:
        """Login method
        :params password: Password for login
        :returns: Token when login is correct and error when is not
        """
        self._validate_password(password)
        self._login_request.params.Password = password
        with self.session_scope():
            request_data = self._prepare_request_data(self._login_request)
            response = self.post(data=request_data)
        response_data = self._handle_response(response)
        self._token = response_data["result"]["token"]
        return self._token

    def _validate_password(self, password: str) -> None:
        if not password:
            raise UserValueError(self.ERROR_MSG_PASSWORD_REQUIRED)
