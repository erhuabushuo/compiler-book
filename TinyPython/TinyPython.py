#!/usr/bin/env python

def parse_execute (input):
    return True

def interactive_shell (prompt='>>> '):
    while True:
        try:
            line = raw_input (prompt)
            ret = parse_execute (line)
            if ret is False:
                break
        except EOFError:
            break

def TinyPython ():
    interactive_shell ()

if __name__ == '__main__':
    TinyPython ()
