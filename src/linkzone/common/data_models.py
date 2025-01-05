from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class LoginParams:
    UserName: str = "admin"
    Password: Optional[str] = None


@dataclass
class LoginRequest:
    jsonrpc: str = "2.0"
    method: str = "Login"
    id: str = "1.1"
    params: LoginParams = field(default_factory=LoginParams)


@dataclass
class SMSParams:
    SMSId: int = -1
    SMSContent: Optional[str] = None
    SMSTime: Optional[str] = None
    PhoneNumber: List[Optional[str]] = field(default_factory=lambda: [None])


@dataclass
class SendSMSRequest:
    jsonrpc: str = "2.0"
    method: str = "SendSMS"
    id: str = "6.6"
    params: SMSParams = field(default_factory=SMSParams)


@dataclass
class USSDParams:
    UssdContent: Optional[str] = None
    UssdType: Optional[str] = None


@dataclass
class USSDCode:
    value: str
    label: str


@dataclass
class SendUSSDRequest:
    jsonrpc: str = "2.0"
    method: str = "SendUSSD"
    id: str = "3.3"
    params: USSDParams = field(default_factory=USSDParams)


@dataclass
class InformationRequest:
    jsonrpc: str = "2.0"
    method: str = "getInfo"
    id: str = "4.4"
    params: Optional[Dict[str, Any]] = None


@dataclass
class GetSystemInfoRequest:
    jsonrpc: str = "2.0"
    method: str = "GetSystemInfo"
    id: str = "13.1"
    params: Optional[Dict[str, Any]] = None


@dataclass
class GetConnectionSettingsRequest:
    jsonrpc: str = "2.0"
    method: str = "GetConnectionSettings"
    id: str = "3.4"
    params: Optional[Dict[str, Any]] = None


@dataclass
class GetConnectionStateRequest:
    jsonrpc: str = "2.0"
    method: str = "GetConnectionState"
    id: str = "3.1"
    params: Optional[Dict[str, Any]] = None


@dataclass
class GetDeviceNewVersionRequest:
    jsonrpc: str = "2.0"
    method: str = "GetDeviceNewVersion"
    id: str = "9.1"
    params: Optional[Dict[str, Any]] = None


@dataclass
class RequestsData:
    Authentication: Dict[str, "LoginRequest"]
    SMS: Dict[str, "SendSMSRequest"]
    USSD: Dict[str, Any]
    Information: Dict[str, "InformationRequest"]


@dataclass
class RequestConfig:
    """Configuration for requests"""

    timeout: int
    backoff_constant: float
    backoff_exponent_base: float
    endpoint_url: str
