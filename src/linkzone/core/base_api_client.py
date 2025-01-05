from typing import Dict, Any, TypeVar, Generic
from contextlib import contextmanager
from linkzone.core.services.request_service import RequestService
from linkzone.common.exceptions import UserValueError

ResponseType = TypeVar("ResponseType", bound=Dict[str, Any])


class BaseAPIClient(Generic[ResponseType]):
    """Base class for all API clients"""

    ERROR_MSG_NEGATIVE_RETRIES = "Number of retries cannot be negative"

    def __init__(self) -> None:
        """Initialize the base API client with a request service"""
        self._request_service = RequestService()

    def __enter__(self) -> "BaseAPIClient[ResponseType]":
        """Enter context manager"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager"""
        self.close()

    def get(self, data: Dict[str, Any], retries: int = 0) -> ResponseType:
        """
        Send GET request
        :param data: Request data
        :param retries: Number of retries
        :return: Response data
        :raises: UserValueError if retries is negative
        """
        self._validate_retries(retries)
        response = self._request_service.get(data, retries)
        return self._handle_response(response)

    def post(self, data: Dict[str, Any], retries: int = 0) -> ResponseType:
        """
        Send POST request
        :param data: Request data
        :param retries: Number of retries
        :return: Response data
        :raises: UserValueError if retries is negative
        """
        self._validate_retries(retries)
        response = self._request_service.post(data, retries)
        return self._handle_response(response)

    def close(self) -> None:
        """Close the current session"""
        if hasattr(self, "_request_service") and self._request_service:
            self._request_service.session.close()

    @contextmanager
    def session_scope(self):
        """
        Context manager for handling session lifecycle
        :yields: Current instance
        """
        try:
            yield self
        finally:
            self.close()

    def _handle_response(self, response: Dict[str, Any]) -> ResponseType:
        """
        Handle and validate response
        :param response: Response data
        :return: Processed response
        :raises: UserValueError if response contains error
        """
        if "error" in response:
            raise UserValueError(response["error"]["message"])
        return response

    def _validate_retries(self, retries: int) -> None:
        """
        Validate the number of retries
        :param retries: Number of retries
        :raises: UserValueError if retries is negative
        """
        if retries < 0:
            raise UserValueError(self.ERROR_MSG_NEGATIVE_RETRIES)

    def _prepare_request_data(self, request_obj: Any) -> Dict[str, Any]:
        """
        Prepare request data by converting the request object to a dictionary
        :param request_obj: Request object
        :return: Dictionary representation of the request object
        """
        return {
            "jsonrpc": request_obj.jsonrpc,
            "method": request_obj.method,
            "id": request_obj.id,
            "params": request_obj.params.__dict__ if request_obj.params else None,
        }
