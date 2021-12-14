import lxml.html
from typing import TextIO
import re


def __add_tm_to_element__(element):
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


def add_tm(inp_file: TextIO) -> str:
    """Add ™-symbol to 6-letter words in html-file"""
    page = lxml.html.parse(inp_file)
    __add_tm_to_element__(page.getroot())
    return lxml.html.tostring(page, pretty_print=True)
