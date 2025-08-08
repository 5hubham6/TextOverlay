# Parser for TXT quote files

from typing import List
from .TextParserInterface import TextParserInterface
from .Quote import Quote

class TXTParser(TextParserInterface):
    """Strategy object for txt files."""

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse txt files to be ingested.
        
        :param (path): path to the txt file that will be ingested.
        """
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        quotes = []
        txt = open(path, 'r')

        for line in txt:
            if line != "":
                parse = line.split('-')
                new_quote = Quote(parse[0].strip(), parse[1].strip())
                quotes.append(new_quote)
        txt.close()

        return quotes
