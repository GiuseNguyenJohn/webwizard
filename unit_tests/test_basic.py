"""Tests for webwizard.py core functionality."""

import tempfile
import unittest
import webwizard

class TestBasic(unittest.TestCase):
    """Test basic features of webwizard"""

    def test_parse_for_flag(self):
        """Test plaintext, rot13, and base64 flag detection"""

        example_text = 'al;kdjlf.s9flsakdctf{flag}laskdj@#$/dfjaos'
        flags = webwizard.parse_for_flag('ctf{', example_text)
        self.assertIn('plaintext flag: ctf{flag}', flags)
        example_text = 'askldf9817*&(  pgs{synt}  alsklkjasdf'
        flags = webwizard.parse_for_flag('ctf{', example_text)
        self.assertIn('rot13 flag: ctf{flag}', flags)
        example_text = 'askldf9817*&(  Y3Rme2ZsYWd9  alsklkjasdf'
        flags = webwizard.parse_for_flag('ctf{', example_text)
        self.assertIn('base64 flag: ctf{flag}', flags)
        
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
        EEE // javascript comment
        """
        

if __name__ == "__main__":
    unittest.main()