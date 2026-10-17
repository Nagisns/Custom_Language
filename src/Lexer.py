
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
    Tokenize source code using character-by-character lexical analysis.

    The lexer processes individual characters and groups them into tokens
    according to the provided LexerConfig.

    It maintains internal buffers for numbers, words, and symbols.
    When a character cannot be included in the current token, the lexer
    finalizes that token and reprocesses the character.

    The lexer tracks line and column positions, recording the starting
    position of each completed token.

    Supported token types:
        NUMBER: A sequence of numeric digits.
        KEYWORD: A reserved word defined in the configuration.
        IDENTIFIER: A name beginning with a letter, followed by
            letters or digits.
        SYMBOL: A supported single-character symbol.
        MULTI_SYMBOLS: A supported two-character symbol.
        UNKNOWN: An unsupported or unrecognized character.

    Attributes:
        config (LexerConfig): Configuration containing supported keywords
            and symbols.
        source_memory (str): Stores the character currently being processed.
        number (str): Buffer for the current numeric token.
        word (str): Buffer for the current keyword or identifier.
        symbols (str): Buffer for a pending symbol.
        line (int): Current line number, starting at 1.
        column (int): Current column number, starting at 1.
        token_column (int): Starting column of the current token.
        tokens (list[Token]): Collection of completed tokens.
    """

    def __init__(self, config: LexerConfig) -> None:
        self.config = config
        self.source_memory: str = ""
        self.number: str = ""
        self.word: str = ""
        self.symbols: str = ""
        self.line: int = 1
        self.column: int = 1
        self.token_column: int = 1
        self.tokens: list[Token] = []

    def process_char(self, check: str) -> None:
        """
        Process a source character and update the lexer state.

        The character is classified according to the current buffer
        and the configured token rules.

        If a pending token cannot accept the character, that token
        is finalized and the character is processed again.

        Spaces are ignored, while newline characters increment
        the line number and reset the column position.

        Args:
            check (str): A single source character to process.
        """
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
                    consumed = self._process_word(check)

                elif check.isdigit():
                    self.token_column = self.column
                    consumed = self._process_number(check)

                elif check == " ":
                    consumed = ProcessResult.CONSUMED

                elif check == "\n":
                    self.column = 1
                    self.line += 1
                    self.source_memory = ""
                    return

                else:
                    self.token_column = self.column
                    self._add_token(TokenType.UNKNOWN, check)
                    consumed = ProcessResult.CONSUMED

            if consumed == ProcessResult.CONSUMED:
                self.column += 1
                self.source_memory = ""

    def finalize(self) -> None:
        """
        Finalize any unfinished tokens remaining in the buffers.

        This method should be called after all source characters
        have been processed.

        Pending numbers, words, and symbols are converted into
        tokens and their corresponding buffers are cleared.
        """
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

        candidate: str = self.symbols + check

        if candidate in self.config.MULTI_SYMBOLS:
            self._add_token(TokenType.MULTI_SYMBOLS, candidate)
            self.symbols = ""
            return ProcessResult.CONSUMED

        self._add_token(TokenType.SYMBOL, self.symbols)
        self.symbols = ""
        return ProcessResult.RETRY
