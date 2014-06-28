class TokenType (object):
    KEY_DEFUN =  "Defun"
    SEMICOLON =  "Semicolon"
    INTEGER   =  "Integer"
    NAME      =  "Name"
    EOF       =  "EOF"
    EQUALS    =  "Equals"
    PLUS      =  "Plus"

class Token (object):
    def __init__ (self, type):
        self.type = type

    def __repr__ (self):
        try:
            repr = "%s [%s]" % (self.type, self.token)
        except AttributeError:
            repr = "%s" % self.type
        finally:
            return repr

class Lexer:
    def __init__ (self, input):
        self.input = input
        self.c = self.input.read (1)

    def parse_number (self):
        tstring = ''
        while self.c and self.c.isdigit ():
            tstring += self.c
            self.c = self.input.read (1)
        token = Token (TokenType.INTEGER)
        token.token = tstring
        return token

    def parse_name (self):
        tstring = ''
        while self.c and self.c.isalpha ():
            tstring += self.c
            self.c = self.input.read (1)
        if tstring == 'defun':
            return Token (TokenType.KEY_DEFUN)
        elif tstring == 'print':
            return Token (TokenType.KEY_PRINT)
        else:
            # if its not a reserved word then its a name
            token = Token (TokenType.NAME)
            token.token = tstring
            return token

    def yylex (self):
        while self.c:
            token = None
            if self.c.isdigit () is True:
                return self.parse_number ()
            elif self.c.isalpha () is True:
                return self.parse_name ()
            elif self.c == ';':
                token = Token (TokenType.SEMICOLON)
            elif self.c == '=':
                token = Token (TokenType.EQUALS)
            elif self.c == '+':
                token = Token (TokenType.PLUS)
            elif self.c == '{':
                token = Token (TokenType.LBRACE)
            elif self.c == '}':
                token = Token (TokenType.RBRACE)
            elif self.c == ',':
                token = Token (TokenType.COMMA)
            elif self.c == '(':
                token = Token (TokenType.LBRACKET)
            elif self.c == ')':
                token = Token (TokenType.RBRACKET)
            self.c = self.input.read (1)
            if token is not None:
                return token
        return Token (TokenType.EOF)
