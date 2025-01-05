from typing import Dict, Any, Optional
import logging
from time import sleep
import requests
from requests.exceptions import RequestException

from linkzone.common.config import Config
from linkzone.common.exceptions import UserValueError
from linkzone.common.data_models import RequestConfig
from linkzone.core.interfaces.request_handler import RequestHandler
from linkzone.core.services.response_service import ResponseService

logger = logging.getLogger(__name__)


class RequestService(RequestHandler):
    """Implementation of RequestHandler interface"""

    def __init__(self) -> None:
        """Initialize request service with configuration"""
        self.session: requests.Session = requests.Session()
        self.config = RequestConfig(
            timeout=Config.TIMEOUT_REQUESTS,
            backoff_constant=Config.BACKOFF_CONSTANT,
            backoff_exponent_base=Config.BACKOFF_EXPONENT_BASE,
            endpoint_url=Config.ENDPOINT_URL,
        )
        self.response_service = ResponseService()

    def send(
        self, data: Dict[str, Any], method: str = "GET", retries: int = 0
    ) -> Dict[str, Any]:
        """Send request with retry logic"""
        if retries < 0:
            raise UserValueError("Number of retries cannot be negative")
        return self._send_request(data, method)

    def get(self, data: Dict[str, Any], retries: int = 0) -> Dict[str, Any]:
        """Send GET request"""
        return self.send(data, "GET", retries)

    def post(self, data: Dict[str, Any], retries: int = 0) -> Dict[str, Any]:
        """Send POST request"""
        return self.send(data, "POST", retries)

    def _send_request(self, data: Dict[str, Any], method: str) -> Dict[str, Any]:
        """Internal method to send request with retry logic"""
        resp: Optional[requests.Response] = None
        success: bool = False
        error: Optional[Exception] = None
        attempts: int = 0

        while not success and attempts <= self.config.timeout:
            try:
                resp = self._attempt_request(data, method, attempts)
                success = True
            except RequestException as e:
                error = e
                logger.debug(f"Request failed: {str(e)}")
                attempts += 1
                if resp is not None:
                    self._log_retry_attempt(resp, attempts)

        if not success:
            self.response_service.handle_error(error)
        return self.response_service.parse_response(resp) if resp else {}

    def _attempt_request(
        self, data: Dict[str, Any], method: str, attempts: int
    ) -> requests.Response:
        """Attempt a single request"""
        if attempts > 0:
            self._apply_backoff(attempts)

        logger.debug(f"Sending {method} request with data: {data}")
        return self.session.request(
            method, self.config.endpoint_url, json=data, timeout=self.config.timeout
        )

    def _apply_backoff(self, attempts: int) -> None:
        """Apply exponential backoff"""
        wait_time = self.config.backoff_constant * (
            self.config.backoff_exponent_base**attempts
        )
        sleep(wait_time)

    def _log_retry_attempt(self, resp: requests.Response, attempts: int) -> None:
        """Log retry attempt details"""
        encoding: str = resp.encoding if resp.encoding is not None else "utf-8"
        logger.debug(
            f"Request failed with status {resp.status_code}. "
            f"Retry attempt {attempts}/{self.config.timeout}\n"
            f"Response: {resp.content.decode(encoding)}"
        )
