source = "let x = 10 + 5"

number = ""
word = ""
symbol = ""

tokens = []

def check_number(check: str) -> None:

    global number

    if check.isdigit():
        number += check
    elif number.isdigit():
        tokens.append(("NUMBER", number))
        print("number ->", number)
        number = ""

def check_word(check: str) -> None:

    global word

    if check.isalpha():
        word += check
    elif word.isalpha():
        tokens.append(("WORD", word))
        print("word ->", word)
        word = ""

def check_symbol(check: str) -> None:

    global symbol

    if check in {"=", "+"}:
        symbol += check
    elif symbol != "":
        tokens.append(("SYMBOL", symbol))
        print("symbol ->" , symbol) 
        symbol = ""

for char in source:

    check_number(char)
    check_word(char)
    check_symbol(char)
    
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
    tokens.append(("WORD", word))
    print("word ->", word)

if symbol != "":
    tokens.append(("SYMBOL", symbol))
    print("symbol ->", symbol)

for token in tokens:
    print(token)
