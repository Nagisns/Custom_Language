# Custom Language

A small programming language project written in Python.

This project aims to create a language with strict static type checking while keeping the syntax simple and easy to read.

## Status

Current version: `v0.0.9`

A class-based stateful lexer has been implemented with separate modules for lexer logic, configuration, token representation, and type definitions. The lexer now tracks source positions and stores generated tokens as objects.

The lexer currently supports tokenization of ASCII source code into numbers, keywords, identifiers, single-character symbols, multi-character symbols, strings, and unknown characters. Identifiers begin with an ASCII letter and may contain ASCII letters or digits after the first character. Outside strings, unsupported ASCII characters are emitted as `UNKNOWN` tokens, while non-ASCII characters raise `SyntaxError` both inside and outside strings.

Double-quoted string literals are emitted as `STRING` tokens. Token values exclude the surrounding double quotes. Empty strings and adjacent string literals are supported. ASCII characters inside strings, including whitespace, operators, and keyword text, are preserved as literal content.

Supported multi-character symbols currently include `==`, `!=`, `+=`, `-=`, `/=`, and `*=`. The lexer temporarily stores a symbol when necessary and checks the following character to determine whether it forms a valid multi-character symbol.

Lexer behavior is managed by the `Lexer` class, while supported keywords, single-character symbols, and multi-character symbols are defined separately in `LexerConfig`. The lexer receives a `LexerConfig` instance when it is created, allowing configuration to be changed without modifying the lexer logic directly.

Generated tokens are represented by the `Token` class defined in `Token.py`. Each token stores its type, value, starting line number, and starting column. The class also provides `__repr__()` to display these details.

Lexer-related type definitions are provided by the `token_types.py` module. This module defines `TokenType` and `ProcessResult` using `Enum`. `TokenType` represents token categories, while `ProcessResult` indicates whether the current character has been consumed or should be processed again.

Source line and column numbers start at 1. Outside strings, ASCII whitespace other than `\n`, including spaces, tabs, and carriage returns, is skipped while advancing the column by one per character. A `\n` outside a string increments the line number and resets the column to 1 without generating a token. String token positions point to the opening double quote.

Escape sequences are not supported. Embedded LF characters inside strings are retained but do not advance the line counter or reset the column, so source position tracking for multiline strings and subsequent tokens is not yet supported.

Token processing remains separated into dedicated internal methods, and token creation is centralized in `_add_token()`. At the end of the source input, `finalize()` emits pending numbers, words, and single-character symbols. String tokens are emitted when the closing double quote is read. An unterminated string remains buffered, and `finalize()` neither emits it nor raises an error. Characters can be reprocessed when they belong to the next token.

Automated lexer tests have been added in `tests/test_lexer.py` using pytest, with test configuration defined in `pyproject.toml`. The tests cover tokenization, source positions, input validation, whitespace handling, token finalization, string values and positions, transitions between strings and other token types, and string state reset. Randomized tests cover quote-free ASCII input and valid string literals separately.

Future development will include CI, string escape processing, unterminated string error reporting, correct source position tracking for multiline strings, further lexer refinement, parsing, AST generation, type checking, and interpretation.
