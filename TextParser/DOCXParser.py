"""A strategy onject for ingesting docx files."""
from typing import List
import docx

from .TextParserInterface import TextParserInterface
from .Quote import Quote

class DOCXParser(TextParserInterface):
    """Strategy object for docx files."""

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse docx files to be ingested.
        
        :param (path): path to the docx file that will be ingested.
        """
        if not cls.can_ingest(path):
            raise Exception('coannot ingest exception')
        
        quotes = []
        doc = docx.Document(path)

        for para in doc.paragraphs:
            if para.text != "":
                parse = para.text.split('-')
                new_quote = Quote(parse[0].strip(' "'), parse[1])
                quotes.append(new_quote)

        return quotes
