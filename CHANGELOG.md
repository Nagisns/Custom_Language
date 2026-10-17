# Changelog

## [0.0.9] - 2026-10-18

### Added

- Added the `STRING` token type for double-quoted string literals.
- Added `_process_string()` with a string buffer and state tracking to recognize opening and closing double quotes.
- Added support for empty strings and adjacent string literals, storing token values without the surrounding quotes.
- Added tests for string values, token positions, transitions between strings and other token types, state reset, repeated finalization, and independent lexer instances.
- Added tests for preserving ASCII whitespace and rejecting non-ASCII characters inside strings.
- Added randomized tests covering 500 valid strings and their surrounding tokens.

### Changed

- Updated `process_char()` to prioritize active string processing, preserving symbols, keywords, and whitespace inside strings as literal content.
- Updated the existing randomized ASCII tests to exclude double quotes, keeping source reconstruction checks separate from string token tests.

## [0.0.8] - 2026-10-17

### Added

- Added input type validation to `process_char()` to raise `TypeError` for non-string inputs.
- Added input length validation to `process_char()` to raise `ValueError` when the input does not contain exactly one character.
- Added ASCII validation to `process_char()` to raise `SyntaxError` for non-ASCII characters, including the character, line number, and column in the error message.
- Added `tests/test_lexer.py` with automated tests for tokenization, source positions, input validation, whitespace handling, and token finalization.
- Added stress tests for long tokens and frequent state transitions, and randomized ASCII tests for source reconstruction and token positions.
- Added `pyproject.toml` with pytest configuration for the `src` import path and `tests` directory.

### Changed

- Updated `process_char()` to use `str.isspace()` instead of checking only literal spaces, allowing tabs, carriage returns, and other ASCII whitespace to be skipped.
- Updated `process_char()` to handle `\n` before checking other whitespace.
- Updated the `Lexer` class docstring to document ASCII-only tokenization, token recognition rules, internal buffers, and whitespace handling.
- Updated the `process_char()` docstring to document input validation, raised exceptions, and column advancement.
- Updated the `finalize()` docstring to clarify token classification, repeated calls, and continued input processing.
- Updated `README.md` to document ASCII input restrictions, whitespace handling, and automated lexer tests.
- Updated the current version in `README.md` to `v0.0.8`.

## [0.0.7] - 2026-10-17

### Added

- Added docstrings to `Lexer.__init__()`, `process_char()`, and `finalize()` to document initialization, character processing, and end-of-input handling.
- Added an explicit `str` type annotation to the multi-character symbol candidate in `_process_symbol()`.

### Changed

- Refactored `process_char()` to use `_process_word()` and `_process_number()` when starting new word and number tokens.
- Centralized column advancement and clearing of `source_memory` in the shared `ProcessResult.CONSUMED` handling for all characters except newlines.
- Simplified unsupported-character handling by passing the current character directly to `_add_token()` when creating an `UNKNOWN` token.
- Reorganized the `Lexer` class docstring to clarify token types, internal buffers, character reprocessing, and source position tracking.

### Removed

- Removed the temporary `unknown` buffer from `Lexer`.

## [0.0.6] - 2026-10-09

### Added

- Added `Token.py` with a `Token` class to store token type, value, line number, and starting column.
- Added `Token.__repr__()` to display token details, including source position.
- Added source position tracking using `line`, `column`, and `token_column`, with line and column numbers starting at 1.
- Added `_add_token()` to centralize token creation and storage.

### Changed

- Replaced tuple-based tokens with `Token` objects in `Lexer.tokens`.
- Changed `TokenType` and `ProcessResult` from `Literal` type aliases to `Enum` classes.
- Updated token classification and processing methods to use enum members instead of string values.
- Changed `_check_keyword()` to return `TokenType` instead of the `WordType` type alias.
- Updated `process_char()` to handle `\n` as a line break, increment the line number, and reset the column to 1 without generating an `UNKNOWN` token.
- Updated the `Lexer` class docstring to document source position tracking and `Token` objects.

### Removed

- Removed the `WordType` type alias from `token_types.py`.
- Removed the tuple-based `Token` type alias from `token_types.py`.

## [0.0.5] - 2026-10-08

### Added

- Added `LexerConfig.py` to manage lexer configuration values such as keywords, single-character symbols, and multi-character symbols.
- Added `token_types.py` to store lexer-related type definitions, including `WordType`, `TokenType`, `Token`, and `ProcessResult`.

### Changed

- Refactored `Lexer` to receive a `LexerConfig` instance through its constructor instead of using configuration values defined directly in `Lexer.py`.
- Updated keyword, symbol, and multi-character symbol checks to use values provided by `LexerConfig`.  
- Updated `main.py` to create a `LexerConfig` instance and pass it to `Lexer`.
- Changed `_check_keyword()` to use the lexer configuration and return the `WordType` type alias.
- Improved type clarity by using `ProcessResult` for lexer processing methods.

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
