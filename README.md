# Custom Language

A small programming language project written in Python.

This project aims to create a language with strict static type checking while keeping the syntax simple and easy to read.

## Status

Current version: `v0.0.3`

A class-based stateful lexer has been implemented.

The lexer currently supports tokenization for numbers, keywords, identifiers, symbols, and unknown characters. Identifiers may contain digits after the first character, and unsupported characters are emitted as `UNKNOWN` tokens.

Lexer state and generated tokens are now managed by the `Lexer` class. Token processing is separated into dedicated internal methods, and unfinished tokens are finalized at the end of the source input using `finalize()`.

The project also uses typed token definitions with `Literal` and type aliases.

Future development will include improved operator handling, parsing, AST generation, type checking, and interpretation.
