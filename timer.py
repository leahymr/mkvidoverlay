#!/usr/bin/env python3
# Michael Leahy, November 13, 2019

import time
from contextlib import contextmanager

class Timer():
    ''' Provides a timer resource.

        USAGE:
        with Timer():

        or
        with Timer() as t1:

        ARGUMENTS:
        message - text printed at the end of the timing

        SUBCLASSES:
        Timer() - timer that counts clock time
        ClockTimer() - another name for Timer()
        CPUTimer() - timer that counts process time

        ATTRIBUTES:
        self.message - modify text of message printed at the end
    '''

    def __init__(self, message: str = 'Time elapsed: '):
        self.message = message
        self._timer = time.perf_counter

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.message!r})')

    def __enter__(self):
        self._init_time = self._timer()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._final_time = self._timer()
        self._delta = (self._final_time - self._init_time) * 1000
        print(self.message + '%.2f ms' % self._delta)
        return False

class ClockTimer(Timer):
    ''' Provides a timer resource that measures clock time. '''

    pass

class CPUTimer(Timer):
    ''' Provides a timer resource that measures processor time. '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._timer = time.process_time


@contextmanager
def timeclock(message: str = 'Time elapsed: '):
    try:
        init_time = time.perf_counter()
        yield init_time
    finally:
        final_time = time.perf_counter()
        delta = (final_time - init_time) * 1000
        print(message + '%.2f ms' % delta)

@contextmanager
def procclock(message: str = 'Time elapsed: '):
    try:
        init_time = time.process_time()
        yield init_time
    finally:
        final_time = time.process_time()
        delta = (final_time - init_time) * 1000
        print(message + '%.2f ms' % delta)
