# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import pytest
import random
import string

from Lexer import Lexer
from LexerConfig import LexerConfig
from token_types import TokenType


def tokenize(source: str):
    lexer = Lexer(LexerConfig())

    for char in source:
        lexer.process_char(char)

    lexer.finalize()
    return lexer.tokens


def snapshot(source: str):
    return [
        (token.token_type, token.value, token.line, token.column)
        for token in tokenize(source)
    ]


# ==========================================
# Basic Lexer Tests
# ==========================================


# 1. Empty input
def test_empty_source():
    assert tokenize("") == []


# 2. Very long identifier
def test_extremely_long_identifier():
    source = "a" * 100_000
    tokens = tokenize(source)

    assert len(tokens) == 1
    assert tokens[0].value == source
    assert tokens[0].token_type == TokenType.IDENTIFIER


# 3. Very long number
def test_extremely_long_number():
    source = "9" * 100_000
    tokens = tokenize(source)

    assert len(tokens) == 1
    assert tokens[0].value == source
    assert tokens[0].token_type == TokenType.NUMBER


# 4. Repeated symbols
def test_repeated_symbols():
    source = "=" * 1000
    tokens = tokenize(source)

    assert "".join(token.value for token in tokens) == source


# 5. Mixed tokens without whitespace
def test_tokens_without_spaces():
    source = "abc123+456def"
    tokens = tokenize(source)

    assert [token.value for token in tokens] == [
        "abc123", "+", "456", "def"
    ]


# 6. Repeated finalize calls
def test_finalize_idempotency():
    lexer = Lexer(LexerConfig())

    for char in "hello":
        lexer.process_char(char)

    lexer.finalize()
    first_result = len(lexer.tokens)

    lexer.finalize()

    assert len(lexer.tokens) == first_result


# 7. Position tracking across lines
def test_multiline_positions():
    assert snapshot("abc\n123\nxyz") == [
        (TokenType.IDENTIFIER, "abc", 1, 1),
        (TokenType.NUMBER, "123", 2, 1),
        (TokenType.IDENTIFIER, "xyz", 3, 1),
    ]


# 8. Multiple adjacent newlines
def test_consecutive_newlines():
    tokens = tokenize("\n\n\nabc")

    assert len(tokens) == 1
    assert tokens[0].line == 4
    assert tokens[0].column == 1


# 9. Multi-character input rejection
def test_reject_multiple_characters():
    lexer = Lexer(LexerConfig())

    with pytest.raises(ValueError):
        lexer.process_char("hello")


# 10. Empty character rejection
def test_reject_empty_character():
    lexer = Lexer(LexerConfig())

    with pytest.raises(ValueError):
        lexer.process_char("")


# 11. Invalid input type
@pytest.mark.parametrize("value", [
    None,
    123,
    [],
    {},
])
def test_invalid_input_type(value):
    lexer = Lexer(LexerConfig())

    with pytest.raises(TypeError):
        lexer.process_char(value)


# 12. Source reconstruction
@pytest.mark.parametrize("source", [
    "abc123+456",
    "a==b",
    "123abc",
    "a!=b",
    "x+=10",
    "abc@123",
])
def test_source_reconstruction(source):
    tokens = tokenize(source)

    reconstructed = "".join(
        token.value for token in tokens
    )

    assert reconstructed == source


# 13. Position tracking after symbols
def test_symbol_positions():
    tokens = tokenize("a+b=c")

    assert [
        (token.value, token.column)
        for token in tokens
    ] == [
        ("a", 1),
        ("+", 2),
        ("b", 3),
        ("=", 4),
        ("c", 5),
    ]


# 14. Token duplication
def test_no_duplicate_tokens():
    tokens = tokenize("a==b")

    assert [token.value for token in tokens] == [
        "a", "==", "b"
    ]


# 15. State isolation
def test_independent_instances():
    first = Lexer(LexerConfig())
    second = Lexer(LexerConfig())

    first.process_char("a")
    second.process_char("b")

    first.finalize()
    second.finalize()

    assert first.tokens[0].value == "a"
    assert second.tokens[0].value == "b"


# ==========================================
# Advanced Lexer Stress Tests
# ==========================================


# 16. CRLF line endings
def test_windows_line_endings():
    tokens = tokenize("abc\r\n123")

    assert [
        (token.value, token.line, token.column)
        for token in tokens
    ] == [
        ("abc", 1, 1),
        ("123", 2, 1),
    ]


# 17. Tab whitespace handling
def test_tab_whitespace():
    tokens = tokenize("abc\t123")

    assert [token.value for token in tokens] == [
        "abc", "123"
    ]


# 18. ASCII and non-ASCII whitespace
@pytest.mark.parametrize("space", [
    "\t",
    "\r",
    "\u00a0",
    "\u2003",
])
def test_unicode_whitespace(space):
    source = f"a{space}b"

    if not space.isascii():
        with pytest.raises(SyntaxError, match="Non-ASCII"):
            tokenize(source)

    else:
        tokens = tokenize(source)

        assert [token.value for token in tokens] == [
            "a", "b"
        ]


# 19. Non-ASCII numeric character rejection
@pytest.mark.parametrize("source", [
    "²",
    "٣",
    "１２３",
])
def test_non_ascii_numbers(source):
    with pytest.raises(SyntaxError, match="Non-ASCII"):
        tokenize(source)


# 20. Unicode combining character rejection
def test_unicode_combining_character():
    source = "cafe\u0301"

    with pytest.raises(SyntaxError, match="Non-ASCII"):
        tokenize(source)


# 21. Null character
def test_null_character():
    tokens = tokenize("abc\x00def")

    assert [token.value for token in tokens] == [
        "abc", "\x00", "def"
    ]

    assert tokens[1].token_type == TokenType.UNKNOWN


# 22. Multiple symbol transitions
def test_complex_symbol_sequence():
    tokens = tokenize("a===b!==c")

    assert [token.value for token in tokens] == [
        "a", "==", "=", "b", "!=", "=", "c"
    ]


# 23. Symbol across newline
def test_symbol_newline_boundary():
    tokens = tokenize("=\n=")

    assert [
        (token.value, token.line, token.column)
        for token in tokens
    ] == [
        ("=", 1, 1),
        ("=", 2, 1),
    ]


# 24. Number across newline
def test_number_newline_boundary():
    tokens = tokenize("123\n456")

    assert [token.value for token in tokens] == [
        "123", "456"
    ]


# 25. Identifier-number transitions
@pytest.mark.parametrize(
    "source, expected",
    [
        ("123abc456", ["123", "abc456"]),
        ("abc123def", ["abc123def"]),
        ("1a2b3c", ["1", "a2b3c"]),
        ("999xyz", ["999", "xyz"]),
    ]
)
def test_number_identifier_transitions(source, expected):
    tokens = tokenize(source)

    assert [token.value for token in tokens] == expected


# 26. Token positions after retry
def test_retry_position_integrity():
    tokens = tokenize("abc+123==xyz")

    assert [
        (token.value, token.column)
        for token in tokens
    ] == [
        ("abc", 1),
        ("+", 4),
        ("123", 5),
        ("==", 8),
        ("xyz", 10),
    ]


# 27. Finalize while symbol is pending
def test_finalize_pending_symbol():
    lexer = Lexer(LexerConfig())

    lexer.process_char("=")
    lexer.finalize()

    assert len(lexer.tokens) == 1
    assert lexer.tokens[0].value == "="


# 28. Continue after finalize
def test_continue_after_finalize():
    lexer = Lexer(LexerConfig())

    lexer.process_char("a")
    lexer.finalize()

    lexer.process_char("b")
    lexer.finalize()

    assert [token.value for token in lexer.tokens] == [
        "a", "b"
    ]


# 29. Repeated keyword boundaries
def test_keyword_boundaries():
    tokens = tokenize("let let1 letter")

    assert [token.value for token in tokens] == [
        "let", "let1", "letter"
    ]

    assert tokens[0].token_type == TokenType.KEYWORD
    assert tokens[1].token_type == TokenType.IDENTIFIER
    assert tokens[2].token_type == TokenType.IDENTIFIER


# 30. Unknown characters between identifiers
def test_multiple_unknown_characters():
    tokens = tokenize("abc@@@def")

    assert [token.value for token in tokens] == [
        "abc", "@", "@", "@", "def"
    ]


# 31. Extremely frequent state transitions
def test_massive_state_transitions():
    source = "a1+2=" * 10_000
    tokens = tokenize(source)

    assert len(tokens) == 40_000

    assert "".join(
        token.value for token in tokens
    ) == source


# 32. Repeated newlines with pending tokens
def test_newline_state_integrity():
    source = "abc\n\n123\n\n+\n\nxyz"
    tokens = tokenize(source)

    assert [
        (token.value, token.line)
        for token in tokens
    ] == [
        ("abc", 1),
        ("123", 3),
        ("+", 5),
        ("xyz", 7),
    ]


# 33. Token location range integrity
def test_token_location_integrity():
    source = "abc+123==xyz"
    tokens = tokenize(source)

    for token in tokens:
        start = token.column - 1
        end = start + len(token.value)

        assert source[start:end] == token.value


# 34. Random ASCII fuzzing
def test_random_ascii_fuzzing():
    rng = random.Random(20261017)

    alphabet = (
        string.ascii_letters
        + string.digits
        + string.punctuation
        + " \t\r\n"
    )

    for _ in range(1000):
        source = "".join(
            rng.choice(alphabet)
            for _ in range(rng.randint(0, 200))
        )

        tokens = tokenize(source)

        reconstructed = "".join(
            token.value for token in tokens
        )

        expected = "".join(
            char for char in source
            if not char.isspace()
        )

        assert reconstructed == expected, (
            f"Source reconstruction failed: {source!r}"
        )

        lines = source.split("\n")

        for token in tokens:
            assert 1 <= token.line <= len(lines)

            line = lines[token.line - 1]
            start = token.column - 1
            end = start + len(token.value)

            assert line[start:end] == token.value, (
                f"Invalid token position: {token!r}"
            )

# Created by ChatGPT
