#!/usr/bin/python3
# coding: utf-8

""" Read YAML metadata and Markdown data from file. YAML metadata contain the
    name of template which will be used for rendering the document. Rendering
    the document has to be done externally. """

import codecs
import pathlib
import os
import os.path
import logging

LOGGER = logging.getLogger(__name__)

# pylint: disable=R0903
class Document():
    """ Wrapper for YAML metadata and Markdown data. """
    def __init__(self):
        self.name = None
        self.path = None
        self.meta = {}  # YAML
        self.markdown = None  # Markdown

    def __repr__(self):
        return "Document('{}')".format(self.name)

    def __getattr__(self, key):
        if key not in self.__dict__:
            return self.meta.get(key)  # Access the metadata as attributes

    def load(self, path):
        """ Load the document from a file. """
        self.path = path

        with codecs.open(path, encoding="utf-8") as page_file:
            for line in page_file:
                if line == "\n":
                    break  # Blank line between YAML and Markdown
                else:
                    key, value = line.split(":")
                    self.meta[key.strip()] = value.strip()  # YAML
            self.markdown = "".join(page_file)  # Markdown

        relative_path = os.path.join(pathlib.Path(path).parts[1:])[0]
        self.name = os.path.splitext(relative_path)[0]
# pylint: enable=R0903

# pylint: disable=C0111
def test_document():
    document = Document()
    document.load("documents/index")
    assert "date" in document.meta
    assert "##" in document.markdown

if __name__ == "__main__":
    import pytest
    import sys
    pytest.main(sys.argv[0] + " -s")
