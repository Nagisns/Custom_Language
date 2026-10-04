# Changelog

## [0.0.2] - 2026-10-04

### Added

- Added `KEYWORD` and `IDENTIFIER` token types to distinguish reserved keywords from identifiers.
- Added the `UNKNOWN` token type for unsupported characters.
- Added `KEYWORDS` and `SYMBOLS` sets to manage recognized keywords and symbols.
- Added `TokenType` using `Literal` to define valid token types.
- Added the `Token` type alias and type annotations for the token list.
- Added support for digits inside identifiers after the first character.
- Added `check_keyword()` to classify words as either `KEYWORD` or `IDENTIFIER`.
- Added temporary character reprocessing with `source_memory` so a character that ends one token can still be processed as the start of the next token.

### Changed

- Replaced the separate `check_number()`, `check_word()`, and `check_symbol()` functions with a unified `lexer()` function.
- Changed generic `WORD` tokens into either `KEYWORD` or `IDENTIFIER` tokens.
- Changed tokenization to track the currently active token through `number`, `word`, and `symbol` state.
- Moved recognized symbols from an inline set to the `SYMBOLS` constant.
- Updated identifier parsing so identifiers can contain both letters and digits after beginning with a letter.
- Updated unsupported non-space characters to produce `UNKNOWN` tokens instead of being silently ignored.

## [0.0.1]

### Added

- Added a minimal lexer implementation.
- Added tokenization for numbers, words, and symbols.
- Added support for multi-character numbers and words.
- Added basic symbol grouping for supported symbols.
- Added token storage for later parsing stages.
- Added `README.md` with a short project overview and current development status.
- Added `CHANGELOG.md` to track version history.
- Added the MIT License.
- Added `.gitignore` for Python development files.
