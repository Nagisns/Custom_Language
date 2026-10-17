# Custom Language

A small programming language project written in Python.

This project aims to create a language with strict static type checking while keeping the syntax simple and easy to read.

## Status

Current version: `v0.0.8`

A class-based stateful lexer has been implemented with separate modules for lexer logic, configuration, token representation, and type definitions. The lexer now tracks source positions and stores generated tokens as objects.

The lexer currently supports tokenization of ASCII source code into numbers, keywords, identifiers, single-character symbols, multi-character symbols, and unknown characters. Identifiers begin with an ASCII letter and may contain ASCII letters or digits after the first character. Unsupported ASCII characters are emitted as `UNKNOWN` tokens, while non-ASCII characters raise `SyntaxError`.

Supported multi-character symbols currently include `==`, `!=`, `+=`, `-=`, `/=`, and `*=`. The lexer temporarily stores a symbol when necessary and checks the following character to determine whether it forms a valid multi-character symbol.

Lexer behavior is managed by the `Lexer` class, while supported keywords, single-character symbols, and multi-character symbols are defined separately in `LexerConfig`. The lexer receives a `LexerConfig` instance when it is created, allowing configuration to be changed without modifying the lexer logic directly.

Generated tokens are represented by the `Token` class defined in `Token.py`. Each token stores its type, value, starting line number, and starting column. The class also provides `__repr__()` to display these details.

Lexer-related type definitions are provided by the `token_types.py` module. This module defines `TokenType` and `ProcessResult` using `Enum`. `TokenType` represents token categories, while `ProcessResult` indicates whether the current character has been consumed or should be processed again.

Source line and column numbers start at 1. ASCII whitespace other than `\n`, including spaces, tabs, and carriage returns, is skipped while advancing the column by one per character. A `\n` increments the line number and resets the column to 1 without generating a token.

Token processing remains separated into dedicated internal methods, and token creation is centralized in `_add_token()`. Unfinished tokens are finalized at the end of the source input using `finalize()`, and characters can be reprocessed when they belong to the next token.

Automated lexer tests have been added in `tests/test_lexer.py` using pytest, with test configuration defined in `pyproject.toml`. The tests cover tokenization, source positions, input validation, whitespace handling, token finalization, and randomized ASCII input.

Future development will include CI, string literals, further lexer refinement, parsing, AST generation, type checking, and interpretation.
