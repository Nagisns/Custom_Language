# Custom Language

A small programming language project written in Python.

This project aims to create a language with strict static type checking while keeping the syntax simple and easy to read.

## Status

Current version: `v0.0.6`

A class-based stateful lexer has been implemented with separate modules for lexer logic, configuration, token representation, and type definitions. The lexer now tracks source positions and stores generated tokens as objects.

The lexer currently supports tokenization for numbers, keywords, identifiers, single-character symbols, multi-character symbols, and unknown characters. Identifiers may contain digits after the first character, and unsupported characters are emitted as `UNKNOWN` tokens.

Supported multi-character symbols currently include `==`, `!=`, `+=`, `-=`, `/=`, and `*=`. The lexer temporarily stores a symbol when necessary and checks the following character to determine whether it forms a valid multi-character symbol.

Lexer behavior is managed by the `Lexer` class, while supported keywords, single-character symbols, and multi-character symbols are defined separately in `LexerConfig`. The lexer receives a `LexerConfig` instance when it is created, allowing configuration to be changed without modifying the lexer logic directly.

Generated tokens are represented by the `Token` class defined in `Token.py`. Each token stores its type, value, starting line number, and starting column. The class also provides `__repr__()` to display these details.

Lexer-related type definitions are provided by the `token_types.py` module. This module defines `TokenType` and `ProcessResult` using `Enum`. `TokenType` represents token categories, while `ProcessResult` indicates whether the current character has been consumed or should be processed again.

Source line and column numbers start at 1. Spaces are skipped while advancing the column, and `\n` is handled as a line break that increments the line number and resets the column to 1 without generating a token.

Token processing remains separated into dedicated internal methods, and token creation is centralized in `_add_token()`. Unfinished tokens are finalized at the end of the source input using `finalize()`, and characters can be reprocessed when they belong to the next token.

Future development will include automated testing and CI, string literals, further lexer refinement, parsing, AST generation, type checking, and interpretation.