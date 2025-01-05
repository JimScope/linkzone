from abc import ABC, abstractmethod
from typing import Dict, Any


class RequestHandler(ABC):
    """Interface for handling HTTP requests"""

    @abstractmethod
    def send(
        self, data: Dict[str, Any], method: str = "GET", retries: int = 0
    ) -> Dict[str, Any]:
        """Send a request"""
        pass

    @abstractmethod
    def get(self, data: Dict[str, Any], retries: int = 0) -> Dict[str, Any]:
        """Send a GET request"""
        pass

    @abstractmethod
    def post(self, data: Dict[str, Any], retries: int = 0) -> Dict[str, Any]:
        """Send a POST request"""
        pass
