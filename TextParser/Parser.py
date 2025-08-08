# Main parser that picks the right helper based on file type

from typing import List
from .Quote import Quote
from .TextParserInterface import TextParserInterface
from .DOCXParser import DOCXParser
from .CSVParser import CSVParser
from .PDFParser import PDFParser
from .TXTParser import TXTParser

class Parser(TextParserInterface):
    # Handles different file types for quotes

    parsers = [TXTParser, DOCXParser, PDFParser, CSVParser]

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        # Pick the right parser and handle errors nicely
        for parser in cls.parsers:
            if parser.can_ingest(path):
                try:
                    return parser.parse(path)
                except Exception as e:
                    print(f"Warning: Could not parse {path}: {e}")
                    return []
        
        print(f"Warning: No suitable parser found for {path}")
        return []
