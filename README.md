# Custom Language

A small programming language project written in Python.

This project aims to create a language with strict static type checking while keeping the syntax simple and easy to read.

## Status

Current version: `v0.0.5`

A class-based stateful lexer has been implemented and refactored to separate lexer logic, configuration, and type definitions.

The lexer currently supports tokenization for numbers, keywords, identifiers, single-character symbols, multi-character symbols, and unknown characters. Identifiers may contain digits after the first character, and unsupported characters are emitted as `UNKNOWN` tokens.

Supported multi-character symbols currently include `==`, `!=`, `+=`, `-=`, `/=`, and `*=`. The lexer temporarily stores a symbol when necessary and checks the following character to determine whether it forms a valid multi-character symbol.

Lexer behavior is managed by the `Lexer` class, while supported keywords, single-character symbols, and multi-character symbols are defined separately in `LexerConfig`. The lexer receives a `LexerConfig` instance when it is created, allowing configuration to be changed without modifying the lexer logic directly. 

Lexer-related type definitions have also been moved to a separate `token_types.py` module. This module defines `WordType`, `TokenType`, `Token`, and `ProcessResult` using `Literal` and type aliases.

Token processing remains separated into dedicated internal methods, unfinished tokens are finalized at the end of the source input using `finalize()`, and characters can be reprocessed when they belong to the next token.

Future development will include source position tracking, automated testing and CI, string literals, further lexer refinement, parsing, AST generation, type checking, and interpretation.