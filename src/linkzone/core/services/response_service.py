from typing import Dict, Any, Optional
import requests
from linkzone.core.interfaces.response_handler import ResponseHandler
from linkzone.common.exceptions import (
    ResponseParseError,
    ResponseServerError,
    ResponseClientError,
    ResponseRedirectError,
    LinkzoneInternalError,
    UserValueError,
)


class ResponseService(ResponseHandler):
    """Implementation of ResponseHandler interface"""

    def parse_response(self, response: requests.Response) -> Dict[str, Any]:
        if response.status_code >= 500:
            raise ResponseServerError(response)
        elif response.status_code >= 400:
            raise ResponseClientError(response)
        elif response.status_code >= 300:
            raise ResponseRedirectError(response)

        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            raise ResponseParseError("Failed to parse JSON response")

        return self._handle_response(response_json)

    def handle_error(self, error: Optional[Exception]) -> None:
        if error is None:
            raise LinkzoneInternalError("Failed to send request but error is None")
        raise error

    def _handle_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        if "error" in response:
            raise UserValueError(response["error"]["message"])
        return response
