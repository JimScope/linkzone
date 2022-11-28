import logging
from time import sleep

import requests
from requests.exceptions import RequestException

from linkzone.common.config import Config
from linkzone.common.exceptions import (
    InternalTypeError,
    LinkzoneInternalError,
    ResponseClientError,
    ResponseRedirectError,
    ResponseServerError,
    UserValueError,
)

ENDPOINT_URL = "http://192.168.1.1/jrd/webapi"

logger = logging.getLogger(__name__)


class RequestsInterface:
    def __init__(self) -> None:
        self.requests_body: dict = Config.get_requests_data()
        self.session = requests.Session()
        self.timeout = 300.0

        # exponential backoff settings
        self.BACKOFF_CONSTANT = 0.1
        self.BACKOFF_EXPONENT_BASE = 1.5

    def _parse_response(self, response: requests.Response) -> dict:
        """Parse response considering its status code

        :param response: Response object
        """
        try:
            if response.status_code >= 500:
                raise ResponseServerError(response)
            elif response.status_code >= 400:
                raise ResponseClientError(response)
            elif response.status_code >= 300:
                raise ResponseRedirectError(response)
            else:
                return response.json()
        except ValueError:
            raise ValueError

    def send(self, data: dict, method: str = "GET", retries: int = 0) -> dict:
        """Send an HTTP request

        :param data: data to send as JSON, dictionary/list to serialize.
        :param method: the HTTP method to use, the default is POST
        :retries: number of times to retry the request on failure. uses exponential backoff

        :returns: Response objects as string
        """
        if retries < 0:
            raise UserValueError(f"retries must be greater than or equal to 0")
        resp: requests.Response | None = None
        success = False
        error = None
        attempts = 0
        while not success and attempts <= retries:
            if attempts > 0:
                if resp is not None:
                    encoding = resp.encoding if resp.encoding is not None else "utf-8"
                    logger.debug(
                        f"Request failed with status {resp.status_code} auto retry {attempts}/{retries}:\n"
                        f"{resp.content.decode(encoding)}"
                    )
                wait_time = self.BACKOFF_CONSTANT * (
                    self.BACKOFF_EXPONENT_BASE**attempts
                )
                sleep(wait_time)
            try:
                logger.debug(f"Sending request: {method}: %s\nData: {data}")
                resp = self.session.request(
                    method, ENDPOINT_URL, json=data, timeout=self.timeout
                )
                success = True
            except (ResponseServerError, ResponseRedirectError, RequestException) as e:
                error = e
                logger.debug(e)

            attempts += 1

        if not success:
            if error is None:
                # should never happen but just in case
                raise LinkzoneInternalError(f"failed to send request but error is None")
            raise error

        if resp is None:
            raise InternalTypeError("Response object was None")

        return self._parse_response(resp)

    def get(self, data: dict, retries: int = 0) -> dict:
        """
        Send a GET requests

        :param data: data to send as JSON, dictionary/list to serialize.
        :param method: the HTTP method to use, the default is POST
        :retries: number of times to retry the request on failure. uses exponential backoff
        """
        return self.send(data, "GET", retries)

    def post(self, data: dict, retries: int = 0) -> dict:
        """
        Send a POST requests

        :param data: data to send as JSON, dictionary/list to serialize.
        :param method: the HTTP method to use, the default is POST
        :retries: number of times to retry the request on failure. uses exponential backoff
        """
        return self.send(data, "POST", retries)
