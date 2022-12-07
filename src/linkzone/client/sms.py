from datetime import datetime

from linkzone.core.requests_interface import RequestsInterface


class SMS(RequestsInterface):
    """
    Class for SMS requests
    """

    def __init__(self) -> None:
        super().__init__()
        self._requests_body_sms = self.requests_body["SMS"]

    def send_sms(self, phone_number: list[str], message: str) -> dict:
        """
        Send SMS to phone number
        :param phone_number: Phone number
        :param message: Message
        :return: Response
        """
        self._requests_body_sms["SendSMS"]["params"]["PhoneNumber"] = [phone_number]
        self._requests_body_sms["SendSMS"]["params"]["SMSContent"] = message
        self._requests_body_sms["SendSMS"]["params"][
            "SMSTime"
        ] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = self.post(self._requests_body_sms["SendSMS"])
        if "error" in response.keys():
            return response["error"]["message"]
        else:
            return response

    def read_sms(self) -> dict:
        raise NotImplementedError
