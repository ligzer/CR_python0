import unittest
from unittest.mock import Mock, MagicMock
from http.client import HTTPSConnection
from http.server import HTTPServer
from ProxyHandler import ProxyHandler
from io import BytesIO
import urllib
from utils import __add_tm_to_element__
import lxml.html

class ProxyTest(unittest.TestCase):

    def setUp(self) -> None:
        """Empty Test"""

    def test_true(self):
        self.assertEqual(True, True)


class RegExpTest(unittest.TestCase):

    def setUp(self) -> None:
        """Empty Test"""

    def test_5_6_7_length_words(self):
        elem_a = lxml.html.fromstring('<div><b>abcdef1</b><b>ab12ef</b><b>ab3de</b></div>')
        __add_tm_to_element__(elem_a)
        self.assertEqual(b'<div><b>abcdef1</b><b>ab12ef&#8482;</b><b>ab3de</b></div>', lxml.html.tostring(elem_a))

    def test_numbers(self):
        elem_a = lxml.html.fromstring('<b>abcdef 123456</b>')
        __add_tm_to_element__(elem_a)
        self.assertEqual(b'<b>abcdef&#8482; 123456</b>', lxml.html.tostring(elem_a))

    def test_dash(self):
        elem_a = lxml.html.fromstring('<b>a-e-f1 abcdef-10 abcdef-abcdef ten-10 abcde_ ab_dc1</b>')
        __add_tm_to_element__(elem_a)
        self.assertEqual(
            b'<b>a-e-f1&#8482; abcdef-10 abcdef-abcdef ten-10&#8482; abcde_ ab_dc1&#8482;</b>',
            lxml.html.tostring(elem_a))

        elem_b = lxml.html.fromstring('<b>a_1_2b</b>')
        __add_tm_to_element__(elem_b)
        self.assertEqual(
            b'<b>a_1_2b&#8482;</b>',
            lxml.html.tostring(elem_b))

if __name__ == '__main__':
    unittest.main()