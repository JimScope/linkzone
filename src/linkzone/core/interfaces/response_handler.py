from abc import ABC, abstractmethod
from typing import Dict, Any
import requests


class ResponseHandler(ABC):
    """Interface for handling HTTP responses"""

    @abstractmethod
    def parse_response(self, response: requests.Response) -> Dict[str, Any]:
        """Parse HTTP response"""
        pass

    @abstractmethod
    def handle_error(self, error: Exception) -> None:
        """Handle request errors"""
        pass
