from typing import Dict, Any
from linkzone.common.data_models import (
    GetSystemInfoRequest,
    GetConnectionSettingsRequest,
    GetConnectionStateRequest,
    GetDeviceNewVersionRequest,
)
from linkzone.core.base_api_client import BaseAPIClient


class Information(BaseAPIClient[Dict[str, Any]]):
    """
    Class for information requests
    """

    def __init__(self) -> None:
        super().__init__()
        self._requests_body_info = {
            "GetSystemInfo": GetSystemInfoRequest(),
            "GetConnectionSettings": GetConnectionSettingsRequest(),
            "GetConnectionState": GetConnectionStateRequest(),
            "GetDeviceNewVersion": GetDeviceNewVersionRequest(),
        }

    def get_system_info(self) -> Dict[str, any]:
        return self._send_information_request("GetSystemInfo")

    def get_connection_settings(self) -> Dict[str, any]:
        return self._send_information_request("GetConnectionSettings")

    def get_connection_state(self) -> Dict[str, any]:
        return self._send_information_request("GetConnectionState")

    def get_device_new_version(self) -> Dict[str, any]:
        return self._send_information_request("GetDeviceNewVersion")

    def _send_information_request(self, method: str) -> Dict[str, any]:
        with self.session_scope():
            request_data = self._requests_body_info[method].__dict__
            response = self.post(data=request_data)
        return self._handle_response(response)
