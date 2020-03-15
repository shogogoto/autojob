from contextlib import contextmanager


class Progress:
    def __init__(self, case):
        self._case    = case
        self._current = None 
        self._processes = []
    
    @property
    def case(self):
        return self._case
    
    @property
    def n_proc(self):
        return len(self._processes)

    # decorator
    def add_proc(self, proc_func):
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

    def advance(self):
        for _ in iter(self._case):
            for proc in self._processes:
                proc(self)
            self._current = None
