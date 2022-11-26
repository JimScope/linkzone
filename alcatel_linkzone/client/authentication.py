from alcatel_linkzone.core.requests_interface import RequestsInterface


class Authentication(RequestsInterface):
    def __init__(self) -> None:
        super().__init__()
        self.token = None

    def login(self, password: str):
        self.requests_body["Authentication"]["Login"]["params"]["Password"] = password
        self.token = self.post(data=self.requests_body["Authentication"]["Login"])[
            "result"
        ]["token"]
        return self.token

    def get_token(self):
        return self.token
