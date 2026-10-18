# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

class LexerConfig:

    """
    Stores configuration values used by the lexer.

    The configuration defines the keywords, single-character symbols,
    and multi-character symbols that the lexer recognizes.

    Attributes:
    -----------
    KEYWORDS : set[str]
        Stores reserved keywords recognized by the lexer.

    SYMBOLS : set[str]
        Stores supported single-character symbols.

    MULTI_SYMBOLS : set[str]
        Stores supported multi-character symbols.
    """

    def __init__(self) -> None:
        self.KEYWORDS: set[str] = {"let"}
        self.SYMBOLS: set[str] = {"+", "-", "*", "/", "=", "!"}
        self.MULTI_SYMBOLS: set[str] = {"==", "!=", "+=", "-=", "/=", "*="}
