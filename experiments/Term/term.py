"""This module contains the Term class."""


class TermInfo:
    """Stores a list of frecuencies and a document frecuency for a term."""

    def __init__(self, frecuencies, doc_frecuency):
        """Initialize the TermInfo object."""
        self.frecuencies: list[int] = frecuencies
        self.doc_frecuency: int = doc_frecuency

    def __str__(self):
        """Return a string representation of the TermInfo object."""
        return f"{self.frecuencies}, Docs: {self.doc_frecuency}"

    def __repr__(self):
        """Return a printable representation of the TermInfo object."""
        return f"TermInfo(frecuencies: {self.frecuencies}, doc_frecuency: {self.doc_frecuency})"
