import subprocess
import os
from datetime import datetime
import threading

env = dict(os.environ)
main_thread_id = threading.get_ident()
command_splitter = '#' * 40
log_splitter = '-' * 40


def get_thread_log():
    current_thread_id = threading.get_ident()
    return f"\nTHREAD: {current_thread_id}" if main_thread_id != current_thread_id else ''


class Command():
    _p = None
    _out = None
    _err = None
    _path = None
    _ignore_exception = False
    _auto_print = False

    def __init__(self, path=None, ignore_exception=None, auto_print=False):
        self._path = path
        self._ignore_exception = ignore_exception
        self._auto_print = auto_print

    def run(self, cmd, path=None, ignore_exception=None):
        cmd = ' '.join(cmd) if isinstance(cmd, list) else cmd
        ignore_exception = self._ignore_exception or ignore_exception
        cmd_path = path or self._path
        try:
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            thread_log = get_thread_log()
            print('\n'.join([
                command_splitter,
                f'[{timestamp}] COMMAND: {cmd}\nPATH: {cmd_path}{thread_log}',
                command_splitter,
            ]))
            self._p = subprocess.Popen(cmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       cwd=cmd_path,
                                       env=env,
                                       shell=True)
            self._out, self._err = self._p.communicate()
            self._out = self._out.decode('utf-8')
            self._err = self._err.decode('utf-8')

            if self._err and not ignore_exception:
                raise Exception(self._err)
        except Exception as ee:
            if ignore_exception:
                self._err = f'exception: {ee}'
            else:
                raise

        if self._auto_print:
            self.print()

        return self

    def result(self):
        return self.stdout() if self._out else self.stderr()

    def results(self):
        return self.stdout().split('\n') if self._out else self.stderr().split('\n')

    def stdout(self):
        return self._out or ''

    def stderr(self):
        return self._err or ''

    def print(self):
        print('\n'.join([
            log_splitter,
            get_thread_log(),
            self.result(),
            log_splitter,
        ]))

        return self
