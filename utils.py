import lxml.html
from typing import TextIO
import re


def __add_tm_to_element__(element: lxml.html.Element) -> None:
    """Add ™-symbol to 6-letter words in lxml element recursively"""
    if element.tag == 'script':
        return  # Ignore in-html scripts content
    if element.text:
        # Add ™-symbol
        # TODO: fix matching words like a_-_-c
        element.text = re.sub(r'([^a-zA-Z-]|^)([a-zA-Z][a-zA-Z0-9_-]{4}[a-zA-Z0-9])([^a-zA-Z0-9_-]|$)', r'\1\2™\3',
                              element.text)
    for child in element.getchildren():
        __add_tm_to_element__(child)


def __change_links__(element: lxml.html.Element) -> None:
    """Replace absolute urls news.ycombinator.com to localhost:8080"""
    for el, par, url, n in element.iterlinks():
        url = el.get(par, None)
        # TODO: Fix for urls with multiple :// sequences
        if url.startswith('http') and url.find('://news.ycombinator.com') != -1:
            el.set(par, url.replace('http://news.ycombinator.com', 'http://localhost:8080'))
            el.set(par, url.replace('https://news.ycombinator.com', 'http://localhost:8080'))
        if el.text:
            el.text = el.text.replace('http://news.ycombinator.com', 'http://localhost:8080')
            el.text = el.text.replace('https://news.ycombinator.com', 'http://localhost:8080')


# TODO: Find better function name
def rebuild_page(inp_file: TextIO) -> str:
    """Replacing content of html-page"""
    # Force using utf-8 encoding
    utf8_parser = lxml.html.HTMLParser(encoding='utf-8')
    page = lxml.html.parse(inp_file, parser=utf8_parser)
    __add_tm_to_element__(page.getroot())
    __change_links__(page.getroot())
    return lxml.html.tostring(page, pretty_print=True)
