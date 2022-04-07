"""Tests for webwizard.py core functionality."""

import unittest
import webwizard

class TestBasic(unittest.TestCase):
    def test_parse_for_flag(self):
        example_text = 'al;kdjlf.s9flsakdctf{flag}laskdj@#$/dfjaos'
        flags = webwizard.parse_for_flag('ctf{', example_text)
        self.assertIn('plaintext flag: ctf{flag}', flags)
        example_text = 'askldf9817*&(  pgs{synt}  alsklkjasdf'
        flags = webwizard.parse_for_flag('ctf{', example_text)
        self.assertIn('rot13 flag: ctf{flag}', flags)
        example_text = 'askldf9817*&(  Y3Rme2ZsYWd9  alsklkjasdf'
        flags = webwizard.parse_for_flag('ctf{', example_text)
        self.assertIn('base64 flag: ctf{flag}', flags)
        
if __name__ == "__main__":
    unittest.main()