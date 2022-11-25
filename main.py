from config import Config
from src.requests_interface import RequestsInterface

class Information(RequestsInterface):
    def __init__(self) -> None:
        super().__init__()

    def get_system_info(self):
        return self.post(data=self.requests_body["Information"]["GetSystemInfo"])

    def get_connection_settings(self):
        return self.post(data=self.requests_body["Information"]["GetConnectionSettings"])

    def get_connection_state(self):
        return self.post(data=self.requests_body["Information"]["GetConnectionState"])

    def get_device_new_version(self):
        return self.post(data=self.requests_body["Information"]["GetDeviceNewVersion"])


class Authentication(RequestsInterface):
    def __init__(self) -> None:
        super().__init__()
        self.token = None

    def login(self, password: str):
        self.requests_body["Authentication"]["Login"]["params"]["Password"] = password
        self.token = self.post(data=self.requests_body["Authentication"]["Login"])['result']['token']
        return self.token
    
    def get_token(self):
        return self.token
