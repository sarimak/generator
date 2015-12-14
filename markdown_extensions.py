#!/usr/bin/python3
# coding: utf-8

""" Register two Markdown extensions which replace <a href=""> and
    <img src=""> with {{ url_for('') }} and {{ resource('') }} placeholders
    which can be rewritten to absolute URLs and path to static resources. """

import markdown
import markdown.inlinepatterns

class UrlForExtension(markdown.Extension):
    """ Custom handler for URL parsing within the Markdown. """
    def extendMarkdown(self, parser, _):
        pattern = UrlForPattern(markdown.inlinepatterns.LINK_RE, parser)
        parser.inlinePatterns["link"] = pattern

class UrlForPattern(markdown.inlinepatterns.LinkPattern):
    """ Delegates mangling of link targets in Markdown to url_for() """
    def handleMatch(self, match):
        anchor = super().handleMatch(match)
        href = anchor.get("href")
        anchor.set("href", "{{{{ url_for('{}') }}}}".format(href))

        return anchor

class ResourceExtension(markdown.Extension):
    """ Custom handler for image parsing within the Markdown. """
    def extendMarkdown(self, parser, _):
        pattern = ResourcePattern(markdown.inlinepatterns.IMAGE_LINK_RE, parser)
        parser.inlinePatterns["image_link"] = pattern

class ResourcePattern(markdown.inlinepatterns.ImagePattern):
    """ Delegates mangling of image sources in Markdown to resource() """
    def handleMatch(self, match):
        img = super().handleMatch(match)
        src = img.get("src")
        img.set("src", "{{{{ resource('{}') }}}}".format(src))

        return img

EXTENSIONS = [UrlForExtension(), ResourceExtension()]

# pylint: disable=C0111
def parse(markup):
    """ Parse the provided Markdown using the custom handlers. """
    return markdown.markdown(markup, extensions=EXTENSIONS)

def test_resource_for_extension():
    assert parse("![desc](picture.png)") == \
        '<p><img alt="desc" src="{{ resource(\'picture.png\') }}" /></p>'

def test_url_for_extension():
    assert parse("#title") == "<h1>title</h1>"
    assert parse("[desc](locator)") == \
        '<p><a href="{{ url_for(\'locator\') }}">desc</a></p>'

if __name__ == "__main__":
    import pytest
    import sys
    pytest.main(sys.argv[0])
