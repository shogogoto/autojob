import unittest
import os

from autojob.progress import Progress
from autojob.progress import extensions


class TestProgressExtension(unittest.TestCase):
    def test_extend(self):
        prog = Progress("abc")
        prog.extend(extensions.Logger())
        prog.advance()
        self.assertTrue(os.path.exists("log.log"))
        
