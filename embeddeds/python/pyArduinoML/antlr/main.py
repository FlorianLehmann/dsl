import sys

from antlr4 import *

from pyArduinoML.antlr.ArduinomlLexer import ArduinomlLexer
from pyArduinoML.antlr.ArduinomlParser import ArduinomlParser

from pyArduinoML.antlr.listener import Listener


def read_stream(filename):
    fs = FileStream(filename)
    lexer = ArduinomlLexer(fs)
    return CommonTokenStream(lexer)


def build_model(stream):
    parser = ArduinomlParser(stream)
    tree = parser.root()
    listener = Listener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    return listener.app


def export_to_code(app):
    print(app)
 

def main(argv):
    print('\n\nRunning the ANTLR compiler for ArduinoML\n')
    filename = argv[1]
    stream = read_stream(filename)
    app = build_model(stream)
    export_to_code(app)
    
    
    
    
 
if __name__ == '__main__':
    main(sys.argv)