# Custom Language

A small programming language project written in Python.

This project aims to create a language with strict static type checking while keeping the syntax simple and easy to read.

## Status

Current version: `v0.0.2`

A basic state-based lexer has been implemented.

The lexer currently supports tokenization for numbers, keywords, identifiers, symbols, and unknown characters. Identifiers may contain digits after the first character, and unsupported characters are emitted as `UNKNOWN` tokens.

The lexer also distinguishes reserved keywords from identifiers and uses typed token definitions with `Literal` and type aliases.

Future development will include improved operator handling, parsing, AST generation, type checking, and interpretation.
