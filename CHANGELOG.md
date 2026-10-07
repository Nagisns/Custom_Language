# Changelog

## [0.0.4] - 2026-10-08

### Added

- Added the `MULTI_SYMBOLS` token type for supported multi-character symbols.
- Added the `MULTI_SYMBOLS` set with support for `==`, `!=`, `+=`, `-=`, `/=`, and `*=`.
- Added `-`, `*`, `/`, and `!` to the supported `SYMBOLS` set.
- Added copyright and MIT License notices to `Lexer.py`.

### Changed

- Changed symbol processing to temporarily store the first symbol while checking whether it forms a supported multi-character symbol with the next character.
- Updated `_process_symbol()` to generate `MULTI_SYMBOLS` tokens when a valid two-character symbol is found.
- Updated `_process_symbol()` so an invalid multi-character combination finalizes only the stored single-character symbol and leaves the current character available for reprocessing.
- Updated `process_char()` to process a pending symbol even when the current character is not itself a supported symbol.
- Renamed the internal `symbol` state to `symbols` to reflect its use in multi-character symbol processing.
- Updated `finalize()` to finalize a remaining single-character symbol at the end of the source input.
- Updated the `Lexer` class docstring to document multi-character symbols and the updated symbol state.

## [0.0.3] - 2026-10-06

### Added

- Added the `Lexer` class to manage lexer state and token generation.
- Added `finalize()` to finalize unfinished tokens at the end of the source input.
- Added `_process_word()`, `_process_number()`, and `_process_symbol()` internal methods to separate token processing logic.
- Added a class docstring documenting supported token types, lexer state, and methods.
- Added a `main()` function and `if __name__ == "__main__":` entry point.

### Changed

- Moved lexer state from global variables into `Lexer` instance attributes.
- Moved generated token storage into `Lexer.tokens`.
- Replaced the standalone `lexer()` function with the `Lexer.process_char()` method.
- Separated the lexer implementation into `Lexer.py` and program execution into `main.py`.
- Changed EOF token handling from module-level logic to the `Lexer.finalize()` method.
- Refactored word, number, and symbol processing into dedicated internal methods to reduce nesting in `process_char()`.
- Simplified `main.py` so it only creates a `Lexer`, processes the source input, finalizes remaining tokens, and prints the resulting token list.

### Removed

- Removed module-level lexer state variables and the global token list.
- Removed the standalone `lexer()` function.
- Removed module-level EOF token finalization logic.
- Removed per-character debug output for numbers, letters, spaces, and symbols.
- Removed token-finalization debug output such as `number ->`, `word ->`, and `symbol ->`.

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
