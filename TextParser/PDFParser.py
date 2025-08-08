"""Strategy object for ingesting pdf files."""

import os
import random
import subprocess

from typing import List

from .TextParserInterface import TextParserInterface
from .Quote import Quote

class PDFParser(TextParserInterface):
    """Stratgey object for docx files."""

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse pdf files to be ingested.
        
        :param (path): path to the pdf file that will be ingested.
        """
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')
        
        tmp = f'./tmp/pdf_to_text.txt'
        cmd = f"pdftotext -layout -nopgbrk {path} {tmp}"
        subprocess.call(cmd, shell=True, stderr=subprocess.STDOUT)
    
        quotes = []
        with open(tmp) as file_ref:
            for line in file_ref.readlines():
                line = line.strip('\n\r').strip()
                if len(line) > 0:
                    parse = line.split('-')
                    new_quote = Quote(parse[0].strip(' "'), parse[1].strip())
                    quotes.append(new_quote)

        os.remove(tmp)
        return quotes
        
