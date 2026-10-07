# Custom Language

A small programming language project written in Python.

This project aims to create a language with strict static type checking while keeping the syntax simple and easy to read.

## Status

Current version: `v0.0.4`

A class-based stateful lexer has been implemented.

The lexer currently supports tokenization for numbers, keywords, identifiers, single-character symbols, multi-character symbols, and unknown characters. Identifiers may contain digits after the first character, and unsupported characters are emitted as `UNKNOWN` tokens.

Supported multi-character symbols currently include `==`, `!=`, `+=`, `-=`, `/=`, and `*=`. The lexer temporarily stores a symbol when necessary and checks the following character to determine whether it forms a valid multi-character symbol.

Lexer state and generated tokens are managed by the `Lexer` class. Token processing is separated into dedicated internal methods, unfinished tokens are finalized at the end of the source input using `finalize()`, and characters can be reprocessed when they belong to the next token.

The project also uses typed token definitions with `Literal` and type aliases.

Future development will include further lexer refinement, parsing, AST generation, type checking, and interpretation.