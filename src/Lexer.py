# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

from LexerConfig import LexerConfig
from Token import Token
from token_types import (
    TokenType,
    ProcessResult,
)

class Lexer:

    """
    Tokenizes source code one character at a time.

    The lexer keeps track of the current token being built and classifies
    source characters into numbers, keywords, identifiers, symbols,
    multi-character symbols, and unknown tokens.

    The lexer also tracks the current line and column position in the source
    and stores the starting column of each token when it is created.

    Token types:
    ------------
    * NUMBER
        A sequence of numeric characters.

    * KEYWORD
        A reserved word defined in the lexer configuration.

    * IDENTIFIER
        A user-defined name that starts with a letter and may contain
        letters or digits.

    * SYMBOL
        A supported single-character symbol defined in the lexer configuration.
        A symbol may be temporarily stored while the lexer checks whether
        it forms a multi-character symbol with the next character.

    * MULTI_SYMBOLS
        A supported multi-character symbol defined in the lexer configuration.

    * UNKNOWN
        A character that does not match any supported token type.

    Attributes:
    -----------
    config : LexerConfig
        Stores the lexer configuration, including supported keywords,
        symbols, and multi-character symbols.

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

    line : int
        Stores the current line number in the source input.

    column : int
        Stores the current column position in the current line.

    token_column : int
        Stores the starting column of the token currently being built.

    tokens : list[Token]
        Stores all completed Token objects.

    Methods:
    --------
    process_char(check)
        Processes one source character and updates the lexer state and
        source position.

    finalize()
        Finalizes any unfinished token remaining at the end of the source.
    """

    def __init__(self, config: LexerConfig) -> None:
        self.config = config
        self.source_memory: str = ""
        self.number: str = ""
        self.word: str = ""
        self.symbols: str = ""
        self.unknown: str = ""
        self.line: int = 1
        self.column: int = 1
        self.token_column: int = 1
        self.tokens: list[Token] = []

    def process_char(self, check: str) -> None:
        self.source_memory: str = check

        while self.source_memory:
            consumed: ProcessResult = ProcessResult.RETRY

            if self.word != "":
                consumed = self._process_word(check)

            elif self.number != "":
                consumed = self._process_number(check)

            elif check in self.config.SYMBOLS or self.symbols != "":
                consumed = self._process_symbol(check)

            else:
                if check.isalpha():
                    self.token_column = self.column
                    self.column += 1
                    self.word += check
                    self.source_memory = ""
                    return
                
                if check.isdigit():
                    self.token_column = self.column
                    self.column += 1
                    self.number += check
                    self.source_memory = ""
                    return
                
                if check == " ":
                    self.column += 1
                    self.source_memory = ""
                    return

                if check == "\n":
                    self.column = 1
                    self.line += 1
                    self.source_memory = ""
                    return

                self.token_column = self.column    
                self.column += 1
                self.unknown += check
                self._add_token(TokenType.UNKNOWN, self.unknown)
                self.unknown = ""
                self.source_memory = ""
                return

            if consumed == ProcessResult.CONSUMED:
                self.column += 1
                self.source_memory = ""

    def finalize(self) -> None:
        if self.number != "":
            self._add_token(TokenType.NUMBER, self.number)
            self.number = ""

        if self.word != "":
            token_type: TokenType = self._check_keyword(self.word)
            self._add_token(token_type, self.word)
            self.word = ""

        if self.symbols != "":
            self._add_token(TokenType.SYMBOL, self.symbols)
            self.symbols = ""

    def _add_token(self, token_type: TokenType, value: str) -> None:
        self.tokens.append(
            Token(token_type, value, self.line, self.token_column)
        )

    def _check_keyword(self, check: str) -> TokenType:
        if check in self.config.KEYWORDS:
            return TokenType.KEYWORD

        return TokenType.IDENTIFIER

    def _process_word(self, check: str) -> ProcessResult:
        if check.isalnum():
            self.word += check
            return ProcessResult.CONSUMED
        
        token_type: TokenType = self._check_keyword(self.word)
        self._add_token(token_type, self.word)
        self.word = ""
        return ProcessResult.RETRY

    def _process_number(self, check: str) -> ProcessResult:
        if check.isdigit():
            self.number += check
            return ProcessResult.CONSUMED
        
        self._add_token(TokenType.NUMBER, self.number)
        self.number = ""
        return ProcessResult.RETRY

    def _process_symbol(self, check: str) -> ProcessResult:
        if self.symbols == "":
            self.token_column = self.column
            self.symbols += check
            return ProcessResult.CONSUMED

        candidate = self.symbols + check

        if candidate in self.config.MULTI_SYMBOLS:
            self._add_token(TokenType.MULTI_SYMBOLS, candidate)
            self.symbols = ""
            return ProcessResult.CONSUMED

        self._add_token(TokenType.SYMBOL, self.symbols)
        self.symbols = ""
        return ProcessResult.RETRY
