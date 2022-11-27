from linkzone.core.requests_interface import RequestsInterface


class Information(RequestsInterface):
    def __init__(self) -> None:
        super().__init__()

    def get_system_info(self):
        return self.post(data=self.requests_body["Information"]["GetSystemInfo"])

    def get_connection_settings(self):
        return self.post(
            data=self.requests_body["Information"]["GetConnectionSettings"]
        )

    def get_connection_state(self):
        return self.post(data=self.requests_body["Information"]["GetConnectionState"])

    def get_device_new_version(self):
        return self.post(data=self.requests_body["Information"]["GetDeviceNewVersion"])
