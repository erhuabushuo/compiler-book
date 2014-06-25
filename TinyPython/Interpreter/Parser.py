import sys

class Parser:
    def __init__ (self, lexer):
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

    def toplevel_declarations (self):
        # can be function of expression or print
        pass

    def parseEval (self):
        # kick things off with the first token
        self.token = self.lexer.yylex ()
        while token is not None:
            toplevel_declarations ()
