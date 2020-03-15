from contextlib import contextmanager
from contextlib import ExitStack


class Progress:
    def __init__(self, case):
        self._case    = case
        self._current = None 
        self._processes = []
        self._contexts  = []
        self._stack = ExitStack()

    @property
    def case(self):
        return self._case
    
    @property
    def n_proc(self):
        return len(self._processes)

    # decorator
    def add_proc(self, cm_func=None, *args, **kwargs):
        self._contexts.append((cm_func, args, kwargs))
        def _add_proc(proc_func):
            # proc_func: (Progress) -> Job, checker
            # これをテストで定義すべし
            def wrapper(progress):
                job, checker = proc_func(progress)
                if self._current is None:
                    state = checker.check(job)
                else:
                    state = self._current.execute(job, checker)
                self._current = state
            self._processes.append(wrapper)
        return _add_proc

    def advance(self):
        for _ in iter(self._case):
            for i, proc in enumerate(self._processes):
                cm_func, args, kwargs = self._contexts[i]
                if cm_func is not None:
                    self._stack.enter_context(cm_func(*args, **kwargs))
                proc(self)
            self._current = None
            self._stack.close()
