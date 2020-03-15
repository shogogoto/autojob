import unittest
from pathlib import Path
import os
from contextlib import contextmanager
from autojob.progress import Progress


class TestChecker:
    def check(self, job):
        return TestState()


class TestState:
    def execute(self, job, checker):
        return TestState()

@contextmanager
def chdir(path):
    old = Path.cwd()
    p = Path(path)
    try:
        p.mkdir(parents=True, exist_ok=True)
        os.chdir(p)
        yield
    finally:
        os.chdir(old)

class TestProgress(unittest.TestCase):
    def setUp(self):
        self.prog = Progress("abcd")
        
        @self.prog.add_proc
        def test_proc1(progress):
            with chdir("proc1"):
                print(os.getcwd())
                progress.test_state = 0
                return "dummy_job", TestChecker()
        
        @self.prog.add_proc
        def test_proc2(progress):
            with chdir("proc2"):
                #print(progress.test_state)
                return "dummy_job", TestChecker()

    def test_n_proc(self):
        self.assertEqual(self.prog.n_proc, 2)

    def test_advance(self):
        print(os.getcwd())
        self.prog.advance()
        print(os.getcwd())
        self.assertTrue(os.path.exists("proc1/proc2"))


