import requests

from alcatel_linkzone.common.config import Config

ENDPOINT_URL = "http://192.168.1.1/jrd/webapi"


class RequestsInterface:
    def __init__(self) -> None:
        self.requests_body: dict = Config.get_requests_data()
        self.session = requests.Session()

    def requests_data(self) -> dict:
        return self.requests_body

    def post(self, data: object) -> dict:
        response = self.session.post(ENDPOINT_URL, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}")
