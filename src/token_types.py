# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

from typing import Literal

WordType = Literal[
    "KEYWORD", 
    "IDENTIFIER"
]

TokenType = Literal[
    "NUMBER",
    "KEYWORD",
    "IDENTIFIER",
    "SYMBOL",
    "MULTI_SYMBOLS",
    "UNKNOWN",
]

Token = tuple[TokenType, str]

ProcessResult = Literal[
    "CONSUMED",
    "RETRY",
]
