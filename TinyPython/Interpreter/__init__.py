from Lexer import Lexer
from Parser import Parser

def evaluate (input):
    lexer = Lexer (input)
    parser = Parser (lexer)
    parser.yyparse ()
