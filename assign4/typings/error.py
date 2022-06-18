from typing import Union


class Err:
    def __init__(self, message: str) -> None:
        self.message = message


Error = Union[Err, None]
