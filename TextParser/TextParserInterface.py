"""Abstract base class for quote parsers using the Strategy Pattern."""

from abc import ABC, abstractmethod
from typing import List
from .Quote import Quote


class TextParserInterface(ABC):
    """Abstract base class defining the interface for quote file processors.
    
    This class implements the Strategy Pattern, allowing different file formats
    to be processed using a consistent interface. Each concrete implementation
    handles a specific file type (CSV, DOCX, PDF, TXT).
    """

    allowed_extensions = []

    @classmethod
    @abstractmethod
    def can_ingest(cls, path: str) -> bool:
        """Determine if this ingestor can process the given file.
        
        Args:
            path (str): The file path to evaluate.

        Returns:
            bool: True if this ingestor can process the file, False otherwise.
        """
        ext = path.split('.')[-1].lower()
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse quotes from the specified file.
        
        Args:
            path (str): The path to the file to parse.

        Returns:
            List[Quote]: A list of Quote instances representing 
                            the quotes found in the file.
                            
        Raises:
            Exception: If the file cannot be parsed or doesn't exist.
        """
        pass
