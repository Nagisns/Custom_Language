from Lexer import Lexer

source = "let x = 10 + 5"

def main() -> None:
    lexer = Lexer()
    
    for char in source:
        lexer.process_char(char)

    lexer.finalize()

    for token in lexer.tokens:
        print(token)

if __name__ == "__main__":
    main()
