from linkzone.core.requests_interface import RequestsInterface


class USSD(RequestsInterface):
    """
    Class for USSD requests
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._requests_body_sms = self.requests_body["USSD"]

    def send_ussd(self, ussd_code: str) -> dict:
        raise NotImplementedError

    def list_ussd_codes(self) -> dict:
        """
        List all the USSD codes available on the json requests_data.json
        :return: List of USSDCodes
        """
        return self._requests_body_sms["USSDCodes"]
