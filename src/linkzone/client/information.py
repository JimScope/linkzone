from linkzone.core.requests_interface import RequestsInterface


class Information(RequestsInterface):
    """
    Class for information requests
    """

    def __init__(self) -> None:
        super().__init__()
        self._requests_body_info = self.requests_body["Information"]

    def get_system_info(self) -> dict:
        return self.post(data=self._requests_body_info["GetSystemInfo"])

    def get_connection_settings(self) -> dict:
        return self.post(data=self._requests_body_info["GetConnectionSettings"])

    def get_connection_state(self) -> dict:
        return self.post(data=self._requests_body_info["GetConnectionState"])

    def get_device_new_version(self) -> dict:
        return self.post(data=self._requests_body_info["GetDeviceNewVersion"])
