"""Implement the Block class."""

from term import TermInfo


class Block:
    """Stores enough records to almost fill PAGE_SIZE."""

    def __init__(self, local_idx: dict[str, TermInfo]):
        """Construct a Block from a dict."""
        self.local_idx: dict[str, TermInfo] = local_idx
