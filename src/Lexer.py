
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
    Tokenize ASCII source code one character at a time.

    Call process_char() for each source character, then finalize() to emit
    any buffered token. Completed tokens are appended to tokens in source
    order according to the provided LexerConfig.

    It maintains internal buffers for numbers, words, and symbols.
    When a character cannot be included in the current token, the lexer
    finalizes that token and reprocesses the character.

    Token positions use one-based line and column numbers. ASCII whitespace
    separates tokens without producing a token. Only a newline (LF) advances
    the line and resets the column to 1; other whitespace, including tabs
    and carriage returns, advances the column by one character.

    Supported token types:
        NUMBER: A sequence of ASCII digits (0-9).
        KEYWORD: An alphanumeric word beginning with an ASCII letter
            that exactly matches a configured keyword.
        IDENTIFIER: An ASCII letter followed by zero or more ASCII letters
            or digits, excluding configured keywords. Underscores are
            not part of identifiers.
        SYMBOL: A supported single-character symbol.
        MULTI_SYMBOLS: A configured two-character symbol whose first
            character is also in config.SYMBOLS.
        UNKNOWN: An ASCII character that is neither alphanumeric,
            whitespace, nor a configured symbol.

    Non-ASCII input is rejected with SyntaxError rather than emitted as
    an UNKNOWN token.

    Attributes:
        config (LexerConfig): Configuration containing supported keywords
            and symbols.
        source_memory (str): Character awaiting consumption, or an empty
            string when no character is pending.
        number (str): Buffer for the current numeric token.
        word (str): Buffer for the current keyword or identifier.
        symbols (str): Buffer for a pending single-character symbol.
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
        Process exactly one ASCII source character and update the state.

        Input is validated before any lexer state is changed.

        The character is classified according to the current buffer
        and the configured token rules.

        If a pending token cannot accept the character, that token
        is finalized and the character is processed again.

        ASCII whitespace is skipped after finalizing any pending token.
        A newline (LF) increments the line number and resets the column to 1.
        Every other consumed character advances the column by one,
        including tabs and carriage returns.

        Args:
            check (str): A single ASCII source character to process.

        Raises:
            TypeError: If check is not a str.
            ValueError: If check does not contain exactly one character.
            SyntaxError: If check is non-ASCII. The error message includes
                the current line and column.
        """
        if not isinstance(check, str):
            raise TypeError(f"Expected str, got {type(check).__name__}")

        if len(check) != 1:
            raise ValueError("Expected exactly one character")

        if not check.isascii():
            raise SyntaxError(
                f"Non-ASCII character {check!r} "
                f"at line {self.line}, column {self.column}"
            )
        
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

                elif check == "\n":
                    self.column = 1
                    self.line += 1
                    self.source_memory = ""
                    return

                elif check.isspace():
                    consumed = ProcessResult.CONSUMED

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

        Pending numbers become NUMBER tokens, words become KEYWORD or
        IDENTIFIER tokens, and a pending single-character symbol becomes
        a SYMBOL token. Each corresponding buffer is then cleared.

        Existing tokens and source positions are preserved. Repeated calls
        without new input have no effect, and process_char() can be called
        again to continue from the current position.
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
