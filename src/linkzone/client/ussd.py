from typing import Dict, List, Any
from linkzone.common.data_models import SendUSSDRequest, USSDCode, USSDParams
from linkzone.common.config import Config
from linkzone.core.base_api_client import BaseAPIClient


class USSD(BaseAPIClient[Dict[str, Any]]):  # Especificar tipo de respuesta
    """
    Class for USSD requests
    """

    def __init__(self) -> None:
        super().__init__()
        self._send_ussd_request: SendUSSDRequest = SendUSSDRequest(params=USSDParams())
        self._ussd_codes: List[USSDCode] = Config.USSD_CODES

    def send_ussd(self, ussd_code: str) -> Dict[str, Any]:
        raise NotImplementedError

    def list_ussd_codes(self) -> List[Dict[str, Any]]:
        """
        List all the USSD codes available
        :return: List of USSDCodes
        """
        return [code.__dict__ for code in self._ussd_codes]
