# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

from Lexer import Lexer
from LexerConfig import LexerConfig

source = "let x = 10 + 5"

def main() -> None:
    config = LexerConfig()
    lexer = Lexer(config)
    
    for char in source:
        lexer.process_char(char)

    lexer.finalize()

    for token in lexer.tokens:
        print(token)

if __name__ == "__main__":
    main()
