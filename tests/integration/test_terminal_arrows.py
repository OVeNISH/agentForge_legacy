import os
from pathlib import Path
import select
import subprocess
import sys
import time
import unittest


@unittest.skipUnless(os.name == 'posix', 'arrow menus use POSIX terminals; other platforms use numbered input')
class TerminalArrowTests(unittest.TestCase):
    def session(self, keys):
        import pty
        import termios

        root = Path(__file__).resolve().parents[2]
        master, slave = pty.openpty()
        original = termios.tcgetattr(slave)
        process = None
        transcript = b''
        try:
            process = subprocess.Popen([sys.executable, '-c',
                "from modernize.terminal import Terminal; print('SELECTED=' + Terminal().choose('Project', ['first', 'second']))"],
                cwd=root, env=dict(os.environ, PYTHONPATH=str(root / 'src'), TERM='xterm-256color', NO_COLOR='1'),
                stdin=slave, stdout=slave, stderr=slave)
            deadline = time.monotonic() + 5
            sent = False
            while time.monotonic() < deadline:
                if select.select([master], [], [], 0.05)[0]:
                    transcript += os.read(master, 65536)
                if not sent and b'Choice:' in transcript:
                    os.write(master, keys)
                    sent = True
                if process.poll() is not None:
                    while select.select([master], [], [], 0)[0]:
                        transcript += os.read(master, 65536)
                    break
            self.assertIsNotNone(process.poll(), transcript.decode(errors='replace'))
            self.assertEqual(termios.tcgetattr(slave), original)
            self.assertIn(b'\x1b[?25h', transcript)
            return process.returncode, transcript
        finally:
            if process is not None and process.poll() is None:
                process.kill()
                process.wait()
            os.close(master)
            os.close(slave)

    def test_arrow_keys_select_and_restore_terminal(self):
        for keys, expected in [(b'\x1b[B\r', b'SELECTED=second'),
                               (b'\x1b[A\r', b'SELECTED=second'),
                               (b'2\r', b'SELECTED=second')]:
            with self.subTest(keys=keys):
                code, transcript = self.session(keys)
                self.assertEqual(code, 0, transcript)
                self.assertIn(expected, transcript)

    def test_eof_restores_terminal(self):
        code, transcript = self.session(b'\x04')
        self.assertNotEqual(code, 0)
        self.assertIn(b'EOFError', transcript)
