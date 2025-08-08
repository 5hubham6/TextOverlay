"""Data model for storing quote information."""


class QuoteModel:
    """Represents a quote with its associated author.
    
    This class encapsulates quote data, providing a structured way to store
    and access quote body text and author information throughout the application.
    """

    def __init__(self, body: str, author: str) -> None:
        """Initialize a new QuoteModel instance.
        
        Args:
            body (str): The main text content of the quote.
            author (str): The author or source of the quote.
        """
        self.body = body.strip()
        self.author = author.strip()
    
    def __str__(self) -> str:
        """Return a string representation of the quote."""
        return f'"{self.body}" - {self.author}'
    
    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return f'QuoteModel(body="{self.body}", author="{self.author}")'
