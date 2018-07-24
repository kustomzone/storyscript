# -*- coding: utf-8 -*-
import os

from .compiler import Compiler
from .parser import Parser


class Story:

    def __init__(self, story):
        self.story = story

    @staticmethod
    def read(path):
        """
        Reads a story
        """
        try:
            with open(path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            abspath = os.path.abspath(path)
            print('File "{}" not found at {}'.format(path, abspath))
            exit()

    @classmethod
    def from_file(cls, path):
        """
        Creates a story from a file source
        """
        return Story(cls.read(path))

    @staticmethod
    def from_stream(stream):
        """
        Creates a story from a stream source
        """
        return Story(stream.read())

    def parse(self, ebnf_file=None, debug=False):
        self.tree = Parser(ebnf_file=ebnf_file).parse(self.story, debug=debug)

    def modules(self):
        """
        Gets the modules of a story from its tree.
        """
        modules = []
        for module in self.tree.find_data('imports'):
            modules.append(module.string.child(0).value[1:-1])
        return modules

    def compile(self, debug=False):
        self.compiled = Compiler.compile(self.tree, debug=debug)

    def lex(self):
        return Parser().lex(self.story)

    def process(self, ebnf_file=None, debug=False):
        self.parse(ebnf_file=ebnf_file, debug=debug)
        self.compile(debug=debug)
        return self.compiled