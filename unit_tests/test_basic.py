"""Tests for webwizard.py core functionality."""

import unittest
import webwizard

class TestBasic(unittest.TestCase):
    def test_parse_for_flag(self):
        example_text = 'al;kdjlf.s@#skadlkfjlak233219flsakdctf{flag}laskdj@#$/dfjaos'
        flags = webwizard.parse_for_flag('ctf{', example_text)
        self.assertIn('ctf{flag}', flags)

if __name__ == "__main__":
    unittest.main()