import requests

from config import Config

ENDPOINT_URL = "http://192.168.1.1/jrd/webapi"


class RequestsInterface:
    def __init__(self) -> None:
        self.requests_body: dict = Config.get_requests_data()

    def requests_data(self) -> dict:
        return self.requests_body

    @staticmethod
    def post(data: object) -> dict:
        response = requests.post(ENDPOINT_URL, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}")


class Information(RequestsInterface):
    def __init__(self) -> None:
        super().__init__()

    def get_system_info(self):
        return self.post(data=self.requests_body["Information"]["GetSystemInfo"])

    def get_connection_setting(self):
        return self.post(data=self.requests_body["Information"]["GetConnectionSetting"])

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
