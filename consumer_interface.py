"""consumindo o servico mockado"""

from abc import ABC, abstractmethod
from typing import Union

# from requests.models import Response


class ConsumerInterface(ABC):
    @abstractmethod
    def get_data(self) -> Union[str, list, dict]:
        """Load in the file for extracting text."""
        pass
