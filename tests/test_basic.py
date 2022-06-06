"""Tests for webwizard.py core functionality."""

import tempfile
import unittest
from webwizard import webwizard

class TestBasic(unittest.TestCase):
    """Test basic features of webwizard"""

    def test_parse_for_flag(self):
        """Test plaintext, rot13, and base64 flag detection"""

        example_text = 'al;kdjlf.s9flsakdctf{flag}laskdj@#$/dfjaos'
        flags = webwizard.parse_for_flag('ctf{', example_text)
        self.assertIn('ctf{flag}', flags["plaintext"])
        example_text = 'askldf9817*&(  pgs{synt}  alsklkjasdf'
        flags = webwizard.parse_for_flag('ctf{', example_text)
        self.assertIn('ctf{flag}', flags["rot13"])
        example_text = 'askldf9817*&(  Y3Rme2ZsYWd9  alsklkjasdf'
        flags = webwizard.parse_for_flag('ctf{', example_text)
        self.assertIn('ctf{flag}', flags["base64"])
        
    def test_get_files_in_dir(self):
        """Will passing the directory ./test/file1, ./test/file2
        return the correct paths?
        """

        # create temporary directory that will be destroyed and will
        # destroy all files in it after program finishes executing
        temp_dir = tempfile.TemporaryDirectory()
        with open(f"{temp_dir.name}/file1", 'w') as f:
            f.write('hi 1')
        with open(f"{temp_dir.name}/file2", 'w') as f:
            f.write('hi 2')
        files = webwizard.get_files_in_dir(temp_dir.name)
        correct_list = [f'{temp_dir.name}/file1', f'{temp_dir.name}/file2']
        for correct_file in correct_list:
            self.assertIn(correct_file, files)
        temp_dir.cleanup()

    def test_extract_comments(self):
        """Will HTML, CSS, and Javascript comments be detected?"""

        text = """
        AAA <!-- html comment --> BBB
        CCC /* css comment */ DDD
        EEE // javascript comment"""
        comments = webwizard.extract_comments(text)
        correct_comments = [' html comment ', '/* css comment */', '// javascript comment']
        for correct_comment in correct_comments:
            self.assertIn(correct_comment, comments)

    def test_parse_file_for_flag(self):
        """Will function return ?"""
        pass
    
    def test_extract_comments_from_file(self):
        """"""
        pass
    
    def test_fuzz_sql(self):
        """"""
        pass

if __name__ == "__main__":
    unittest.main()
