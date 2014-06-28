import sys

from Lexer import TokenType

class Parser:
    def __init__ (self, lexer, backend = None):
        self.lexer = lexer
        self.backend = backend
        self.token = self.lexer.yylex ()

    def backend_push (self, ast):
        if self.backend is not None:
            self.backend.push (ast)
        else:
            print ast

    def yyerror (self, message):
        print >>sys.stderr, "Syntax Error: %s" % message

    def parse_accept (self, token, fwd=True):
        if self.token.T == token:
            if fwd == True:
                self.token = self.lexer.yylex ()
            return True
        else:
            return False

    def parse_expect (self, token):
        if self.parse_accept (token) is True:
            return True
        else:
            yyerror ("expected token [%s] got [%s]" % (token, self.token))
            return False

    def expression (self):
        pass

    def print_statement (self):
        pass

    def toplevel_declaration (self):
        return self.expression ()

    def parseEval (self):
        while self.token.type is not TokenType.EOF:
            ast = self.toplevel_declaration ()
            # syntax error just stop
            if ast is None:
                break
            self.backend_push (ast)
