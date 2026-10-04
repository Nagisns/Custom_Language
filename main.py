from typing import Literal

source = "let x = 10 + 5"

number = ""
word = ""
symbol = ""
unknown = ""

KEYWORDS: set[str] = {"let"}

SYMBOLS: set[str] = {"+", "="}

TokenType = Literal[
    "NUMBER",
    "KEYWORD",
    "IDENTIFIER",
    "SYMBOL",
    "UNKNOWN"
]

Token = tuple[TokenType, str]
tokens: list[Token] = []

def check_keyword(check: str) -> Literal["KEYWORD", "IDENTIFIER"]:
    if check in KEYWORDS:
        return "KEYWORD"

    return "IDENTIFIER"

def lexer(check: str) -> None:
    
    global number, word, symbol, unknown
    source_memory: str = check

    while source_memory:
        if word != "":
            if check.isalnum():
                word += check
                source_memory = ""
            else:
                token_type: Literal["KEYWORD", "IDENTIFIER"] = check_keyword(word)
                tokens.append((token_type, word))
                word = ""
        elif number != "":
            if check.isdigit():
                number += check
                source_memory = ""
            else:
                tokens.append(("NUMBER", number))
                number = ""
        elif symbol != "":
            if check in SYMBOLS:
                symbol += check
                source_memory = ""
            else:
                tokens.append(("SYMBOL", symbol))
                symbol = ""
        else:
            if check.isalpha():
                word += check
                source_memory = ""
            elif check.isdigit():
                number += check
                source_memory = ""
            elif check in SYMBOLS:
                symbol += check
                source_memory = ""
            else:
                if check == " ":
                    source_memory = ""
                else:
                    unknown += check
                    tokens.append(("UNKNOWN", unknown))
                    unknown = ""
                    source_memory = ""

for char in source:

    lexer(char)
    
    if char.isdigit():
        print(char, "-> number")
    elif char.isalpha():
        print(char, "-> letter")
    elif char == " ":
        print(char, "-> space")
    else:
        print(char, "-> symbol")

if number != "":
    tokens.append(("NUMBER", number))
    print("number ->", number)

if word != "":
    token_type = check_keyword(word)
    tokens.append((token_type, word))

    print("word ->", word)
    word = ""

if symbol != "":
    tokens.append(("SYMBOL", symbol))
    print("symbol ->", symbol)

for token in tokens:
    print(token)
