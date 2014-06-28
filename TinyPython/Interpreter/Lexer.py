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
        repr = "%s" % self.type
        try:
            repr += " [%s]" % self.token
        except AttributeError:
            pass
        return repr

class Lexer:
    def __init__ (self, input):
        self.input = input

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
        else:
            token = Token (TokenType.NAME)
            token.token = tstring
            return token

    def __iter__ (self):
        self.c = self.input.read (1)
        while self.c:
            if self.c.isdigit () is True:
                yield self.parse_number ()
            if self.c.isalpha () is True:
                yield self.parse_name ()
            elif self.c == ';':
                yield Token (TokenType.SEMICOLON)
            elif self.c == '=':
                yield Token (TokenType.EQUALS)
            elif self.c == '+':
                yield Token (TokenType.PLUS)
            self.c = self.input.read (1)
        yield Token (TokenType.EOF)
