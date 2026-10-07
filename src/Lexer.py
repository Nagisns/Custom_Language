# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

from typing import Literal

TokenType = Literal[
    "NUMBER",
    "KEYWORD",
    "IDENTIFIER",
    "SYMBOL",
    "MULTI_SYMBOLS",
    "UNKNOWN",
]

KEYWORDS: set[str] = {"let"}
SYMBOLS: set[str] = {"+", "-", "*", "/", "=", "!"}
MULTI_SYMBOLS: set[str] = {"==", "!=", "+=", "-=", "/=", "*="}

Token = tuple[TokenType, str]

class Lexer:

    """
    Tokenizes source code one character at a time.

    The lexer keeps track of the current token being built and classifies
    source characters into numbers, keywords, identifiers, symbols,
    multi-character symbols, and unknown tokens.

    Token types:
    ------------
    * NUMBER
        A sequence of numeric characters.

    * KEYWORD
        A reserved word defined in KEYWORDS.

    * IDENTIFIER
        A user-defined name that starts with a letter and may contain
        letters or digits.

    * SYMBOL
        A supported single-character symbol defined in SYMBOLS.
        A symbol may be temporarily stored while the lexer checks whether
        it forms a multi-character symbol with the next character.

    * MULTI_SYMBOLS
        A supported multi-character symbol defined in MULTI_SYMBOLS.

    * UNKNOWN
        A character that does not match any supported token type.

    Attributes:
    -----------
    source_memory : str
        Temporarily stores the current character until it has been fully
        processed.

    number : str
        Stores the NUMBER token currently being built.

    word : str
        Stores the word currently being built before it is classified as
        KEYWORD or IDENTIFIER.

    symbols : str
        Temporarily stores a symbol while checking whether it forms a
        multi-character symbol with the next character.

    unknown : str
        Temporarily stores an unsupported character.

    tokens : list[Token]
        Stores all completed tokens.

    Methods:
    --------
    check_keyword(check)
        Classifies a completed word as KEYWORD or IDENTIFIER.

    process_char(check)
        Processes one source character and updates the current lexer state.

    finalize()
        Finalizes any unfinished token remaining at the end of the source.
    """

    def __init__(self) -> None:
        self.source_memory: str = ""
        self.number: str = ""
        self.word: str = ""
        self.symbols: str = ""
        self.unknown: str = ""
        self.tokens: list[Token] = []

    @staticmethod
    def check_keyword(check: str) -> Literal["KEYWORD", "IDENTIFIER"]:
        if check in KEYWORDS:
            return "KEYWORD"

        return "IDENTIFIER"

    def finalize(self) -> None:
        if self.number != "":
            self.tokens.append(("NUMBER", self.number))
            self.number = ""

        if self.word != "":
            token_type = self.check_keyword(self.word)
            self.tokens.append((token_type, self.word))
            self.word = ""

        if self.symbols != "":
            self.tokens.append(("SYMBOL", self.symbols))
            self.symbols = ""

    def _process_word(self, check: str) -> None:
        if check.isalnum():
            self.word += check
            self.source_memory = ""
            return
        
        token_type: Literal["KEYWORD", "IDENTIFIER"] = self.check_keyword(self.word)
        self.tokens.append((token_type, self.word))
        self.word = ""

    def _process_number(self, check: str) -> None:
        if check.isdigit():
            self.number += check
            self.source_memory = ""
            return
        
        self.tokens.append(("NUMBER", self.number))
        self.number = ""

    def _process_symbol(self, check: str) -> None:
        if self.symbols == "":
            self.symbols += check
            self.source_memory = ""
            return

        candidate = self.symbols + check

        if candidate in MULTI_SYMBOLS:
            self.tokens.append(("MULTI_SYMBOLS", candidate))
            self.symbols = ""
            self.source_memory = ""
            return

        self.tokens.append(("SYMBOL", self.symbols))
        self.symbols = ""

    def process_char(self, check: str) -> None:
        self.source_memory: str = check

        while self.source_memory:
            if self.word != "":
                self._process_word(check)

            elif self.number != "":
                self._process_number(check)

            elif check in SYMBOLS or self.symbols != "":
                self._process_symbol(check)

            else:
                if check.isalpha():
                    self.word += check
                    self.source_memory = ""
                    return
                
                if check.isdigit():
                    self.number += check
                    self.source_memory = ""
                    return
                
                if check == " ":
                    self.source_memory = ""
                    return
                    
                self.unknown += check
                self.tokens.append(("UNKNOWN", self.unknown))
                self.unknown = ""
                self.source_memory = ""
