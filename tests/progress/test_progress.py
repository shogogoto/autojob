import unittest
from pathlib import Path
import os
import shutil
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
        
        @self.prog.add_proc(chdir, "proc1")
        def test_proc1(progress):
            progress.test_state = 0
            print("proc1", os.getcwd())
            return "dummy_job", TestChecker()
        
        @self.prog.add_proc(chdir, "proc2")
        def test_proc2(progress):
            print("prco2", os.getcwd())
            return "dummy_job", TestChecker()

    def test_n_proc(self):
        self.assertEqual(self.prog.n_proc, 2)

    def test_advance(self):
        self.prog.advance()
        self.assertTrue(os.path.exists("proc1/proc2"))
        shutil.rmtree("proc1")

    def test_init(self):
        @self.prog.add_proc(chdir, "a")
        def test_case_a(progress):
            return "dummy_job", TestChecker()
        
        @self.prog.add_proc(chdir, "b")
        def test_case_b(progress):
            return "dummy_job", TestChecker()
        
        @self.prog.add_proc(chdir, "c")
        def test_case_c(progress):
            return "dummy_job", TestChecker()

        self.prog.advance()
        self.assertTrue(os.path.exists("proc1/proc2/a/b/c"))
        shutil.rmtree("proc1")



