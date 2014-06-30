import sys

from Lexer import TokenType

class ParseExpection (Exception):
    def __init__ (self, message):
        self.message = message

class Parser:
    def __init__ (self, lexer, backend = None):
        self.lexer = lexer
        self.backend = backend
        self.token = self.lexer.yylex ()

    def backend_push (self, ast):
        try:
            self.backend.push (ast)
        except AttributeError:
            pass

    def yyerror (self, message):
        print >>sys.stderr, "Syntax Error: %s" % message

    def parse_peek (self, token):
        if self.token.type is token:
            return True
        else:
            return False

    def parse_accept (self, token):
        if self.parse_peek (token) is True:
            self.token = self.lexer.yylex ()
            return True
        else:
            return False

    def parse_expect (self, token):
        if self.parse_accept (token) is True:
            return True
        else:
            raise ParseExpection ("expected token [%s] got [%s]" % (token, self.token))

    def primary_expr (self):
        pass

    def expression (self):
        self.primary_expr ()
        while self.token.type in [ TokenType.PLUS ]:
            self.parse_expect (self.token.type)
            self.primary ()

    def statement (self):
        if self.parse_peek (TokenType.KEY_PRINT):
            return self.print_statement ()
        else:
            return self.expression ()

    def statement_list (self):
        if self.parse_peek (TokenType.RBRACKET):
            return None
        self.statement ()
        self.statement_list ()

    def suite (self):
        self.statement_list ()

    def parameter_list (self):
        pass

    def fndecl (self):
        self.parse_expect (TokenType.KEY_DEFUN)
        self.parse_expect (TokenType.NAME)
        self.parse_expect (TokenType.LBRACE)
        self.parameter_list ()
        self.parse_expect (TokenType.RBRACE)
        self.parse_expect (TokenType.LBRACKET)
        self.suite ()
        self.parse_expect (TokenType.RBRACKET)

    def toplevel_declaration (self):
        """
        S -> lambda : funcdecl | statement
        """
        if self.parse_peek (TokenType.KEY_DEFUN):
            return self.fndecl ()
        else:
            return self.statement ()

    def yyparse (self):
        try:
            while self.token.type is not TokenType.EOF:
                ast = self.toplevel_declaration ()
                # check just for debugging for now
                if ast is None:
                    break
                self.backend_push (ast)
        except ParseExpection as e:
            self.yyerror (e.message)
