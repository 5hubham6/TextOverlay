# Parser for CSV quote files
from typing import List
import pandas

from .TextParserInterface import TextParserInterface
from .Quote import Quote
class CSVParser(TextParserInterface):
    """Strategy object for csv files."""

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse csv files to be ingested.
        
        :param (path): path to the csv file that will be ingested.
        """
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')
        
        quotes = []

        csv = pandas.read_csv(path, header=0)

        for index, row in csv.iterrows():
            new_quote =  Quote(row['body'], row['author'])
            quotes.append(new_quote)

        return quotes
