import sys

class Term:
    def __init__(self) -> None:
        self.df: int
        self.docs: list[tuple[str, int]]

class IdxBlock:
    def __init__(self) -> None:
        self.index: dict[int, Term]

    def add(self, id_term: int, doc: tuple) -> None:
        term = self.index.get(id_term, Term())
        term.docs.append(doc)
        term.df += 1
        self.index[id_term] = term

    def merge(self) -> None:
        pass

    def clear(self) -> None:
        self.index.clear()

    def __sizeof__(self) -> int:
        return sys.getsizeof(self.index)