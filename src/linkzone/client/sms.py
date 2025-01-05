from datetime import datetime
from typing import Dict, List, Any

from linkzone.common.exceptions import UserValueError
from linkzone.common.data_models import SendSMSRequest, SMSParams
from linkzone.core.base_api_client import BaseAPIClient


class SMS(BaseAPIClient[Dict[str, Any]]):  # Especificar tipo de respuesta
    """
    Class for SMS requests
    """

    ERROR_MSG_PHONE_NUMBER_REQUIRED = "Phone number must be provided"
    ERROR_MSG_MESSAGE_REQUIRED = "Message must be provided"

    def __init__(self) -> None:
        super().__init__()
        self._send_sms_request: SendSMSRequest = SendSMSRequest(params=SMSParams())

    def send_sms(self, phone_numbers: List[str], message: str) -> Dict[str, any]:
        """
        Send SMS to phone numbers
        :param phone_numbers: List of phone numbers
        :param message: Message
        :return: Response
        """
        self._validate_phone_numbers(phone_numbers)
        self._validate_message(message)
        self._prepare_sms_request(phone_numbers, message)
        with self.session_scope():
            response = self.post(data=self._send_sms_request.__dict__)
        return self._handle_response(response)

    def _validate_phone_numbers(self, phone_numbers: List[str]) -> None:
        if not phone_numbers:
            raise UserValueError(self.ERROR_MSG_PHONE_NUMBER_REQUIRED)

    def _validate_message(self, message: str) -> None:
        if not message:
            raise UserValueError(self.ERROR_MSG_MESSAGE_REQUIRED)

    def _prepare_sms_request(self, phone_numbers: List[str], message: str) -> None:
        self._send_sms_request.params.PhoneNumber = phone_numbers
        self._send_sms_request.params.SMSContent = message
        self._send_sms_request.params.SMSTime = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def read_sms(self) -> Dict[str, any]:
        raise NotImplementedError
