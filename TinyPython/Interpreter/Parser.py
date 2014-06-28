import sys

from Lexer import TokenType

class Parser:
    def __init__ (self, lexer, backend = None):
        self.lexer = lexer
        self.backend = backend
        self.token = self.lexer.yylex ()

    def backend_push (self, ast):
        if self.backend is None:
            print ast
        else:
            self.backend.push (ast)

    def yyerror (self, message):
        print >>sys.stderr, "Syntax Error: %s" % message

    def parse_peek (self, token):
        if self.token.type is token:
            return True
        else:
            return False

    def parse_accept (self, token):
        if self.parse_peek (token) is True:
            # advance the token stream
            self.token = self.lexer.yylex ()
            return True
        else:
            return False

    def parse_expect (self, token):
        if self.parse_accept (token) is True:
            return True
        else:
            self.yyerror ("expected token [%s] got [%s]" % (token, self.token))
            return False

    def primary (self):
        pass

    def expression (self):
        pass

    def print_statement (self):
        pass

    def function_declaration (self):
        pass

    def toplevel_declaration (self):
        pass

    def yyparse (self):
        while self.token.type is not TokenType.EOF:
            ast = self.toplevel_declaration ()
            # syntax error just stop
            if ast is None:
                break
            self.backend_push (ast)
