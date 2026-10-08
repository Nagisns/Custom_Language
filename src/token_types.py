# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

from enum import Enum

class TokenType(Enum):

    """
    Represents the types of tokens produced by the lexer.
    """

    NUMBER = "NUMBER"
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    SYMBOL = "SYMBOL"
    MULTI_SYMBOLS = "MULTI_SYMBOLS"
    UNKNOWN = "UNKNOWN"

class ProcessResult(Enum):

    """
    Represents whether the current source character was consumed
    or should be processed again.
    """

    CONSUMED = "CONSUMED"
    RETRY = "RETRY"
