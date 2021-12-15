import lxml.html
from typing import TextIO, List
import re

__regexp_url__ = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:\/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.][a-z]{2,4}\/)'
                            r'(?:[^\s\(\)<>]+|\((?:[^\s\(\)<>]+|(?:\([^\s\(\)<>]+\)))*\))+'
                            r'(?:\((?:[^\s\(\)<>]+|(?:\([^\s\(\)<>]+\)))*\)|[^\s`!\(\)\[\]{};:\'".,<>?«»“”‘’]))')

__regexp_domain__ = re.compile(r'([\w-]+(?:\.[\w-]+)+)')
__regexp_dash_underline__ = re.compile(r'(-_+|_+-)')
__regexp_6letter_word__ = re.compile(r'(?i)(?<![\w-])([a-z][\w-]{4}[a-z0-9])(?![\w-])')


def __split_to_words__(text: str) -> List:
    """Split text with rexexp's recursively"""

    # Split by any url-like sequence
    # Example: anyprotocol://yaras.ru/asddas?asd=1&asd=dsa
    splited1 = enumerate(__regexp_url__.split(text))
    for i, t1 in splited1:
        if i % 2 == 0:
            # Split by any domain-like sequence
            # Example: domasd.ads.d.sd.d.ru
            splited2 = enumerate(__regexp_domain__.split(t1))
            for j, t2 in splited2:
                if j % 2 == 0:
                    # Split by any dash-underline sequence
                    # Example: __-
                    splited3 = enumerate(__regexp_dash_underline__.split(t2))
                    for z, t3 in splited3:
                        if z % 2 == 0:
                            yield 'value', t3
                        else:
                            yield 'splitter', t3
                else:
                    yield 'splitter', t2
        else:
            yield 'splitter', t1



def __add_tm_to_element__(element: lxml.html.Element) -> None:
    """Add ™-symbol to 6-letter words in lxml element recursively"""
    if element.tag == 'script':
        return  # Ignore in-html scripts content
    if element.text:
        text = ''
        for k, v in __split_to_words__(element.text):
            if k == 'value':
                # Add ™-symbol to words
                text += __regexp_6letter_word__.sub(r'\1™', v)
            else:
                text += v
        # TODO: Should rename function or refactor, because it's do additinal work
        text = text.replace('http://news.ycombinator.com', 'http://localhost:8080')
        text = text.replace('https://news.ycombinator.com', 'http://localhost:8080')
        element.text = text

    for child in element.getchildren():
        __add_tm_to_element__(child)


def __change_links__(element: lxml.html.Element) -> None:
    """Replace absolute urls news.ycombinator.com to localhost:8080"""
    for el, par, url, n in element.iterlinks():
        url = el.get(par, None)
        # TODO: Fix for urls with multiple :// sequences
        if url.startswith('http') and url.find('://news.ycombinator.com') != -1:
            url = url.replace('http://news.ycombinator.com', 'http://localhost:8080')
            el.set(par, url.replace('https://news.ycombinator.com', 'http://localhost:8080'))


# TODO: Find better function name
def rebuild_page(inp_file: TextIO) -> str:
    """Replacing content of html-page"""
    # Force using utf-8 encoding
    utf8_parser = lxml.html.HTMLParser(encoding='utf-8')
    page = lxml.html.parse(inp_file, parser=utf8_parser)
    __add_tm_to_element__(page.getroot())
    __change_links__(page.getroot())
    return lxml.html.tostring(page, pretty_print=False)
