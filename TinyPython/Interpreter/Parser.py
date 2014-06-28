import sys

from Lexer import TokenType

class Parser:
    def __init__ (self, lexer, backend = None):
        self.lexer = lexer
        self.token = None

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
            yyerror ("expected token [%s] got [%s]" \
                     % (self.lexer.TokenString (token),
                        self.lexer.TokenString (self.token.T)))
            return False

    def parseEval (self):
        for i in self.lexer:
            print i
