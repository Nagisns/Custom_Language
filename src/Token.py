# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

from token_types import TokenType

class Token:

    """
    Represents a single token produced by the lexer.

    Each token stores its type, value, and starting position
    in the source code.

    Attributes:
    -----------
    token_type : TokenType
        The type of the token.

    value : str
        The original text represented by the token.

    line : int
        The line number where the token starts.

    column : int
        The column number where the token starts.

    Methods:
    --------
    __repr__()
        Returns a string representation of the token,
        including its type, value, line, and column.
    """

    def __init__(self, token_type: TokenType, value: str, line: int, column: int) -> None:
        self.token_type: TokenType = token_type
        self.value: str = value
        self.line: int = line
        self.column: int = column

    def __repr__(self) -> str:
        return (
            f"Token("
            f"type={self.token_type.name}, "
            f"value={self.value!r}, "
            f"line={self.line}, "
            f"column={self.column}"
            f")"
        )
