#!/usr/bin/env python

import sys
import optparse
import Interpreter

from cStringIO import StringIO

def TinyShell (prompt='>>> '):
    while True:
        try:
            line = raw_input (prompt)
            buffer = StringIO (line)
            Interpreter.evaluate (buffer)
            buffer.close ()
        except EOFError:
            break

def PrintVersion ():
    print "TinyPython version 0.1"

def TinyPython ():
    parser = optparse.OptionParser ()
    parser.add_option ("-v", "--version", dest='version', default=False,
                       help="Print version", action="store_true")
    (options, args) = parser.parse_args ()
    if options.version is True:
        PrintVersion ()
        return
    if len (args) > 0:
        try:
            with open (args [0], 'r') as fd:
                Interpreter.evaluate (fd)
        except IOError:
            print >>sys.stderr, 'Unable to open [%s]' % args [0]
    else:
        TinyShell ()

if __name__ == '__main__':
    TinyPython ()
