"""Terminal input and observed pipeline progress; no execution decisions."""

import codecs
import os
import select
import sys


STAGES = {'analysis': 'Analyze original code', 'characterization': 'Record legacy behavior',
          'baseline': 'Measure the modern-runtime baseline', 'documentation': 'Generate documentation',
          'conversion': 'Convert source to Python 3', 'repair': 'Verify and repair conversion',
          'heldout': 'Check sealed held-out cases'}


def interactive():
    return os.name == 'posix' and sys.stdin.isatty() and sys.stdout.isatty() and os.environ.get('TERM') != 'dumb'


def clear_rows(count):
    if count:
        sys.stdout.write(f'\033[{count}A\033[J')
        sys.stdout.flush()


def arrow_choice(terminal, label, choices):
    import termios
    import tty

    descriptor = sys.stdin.fileno()
    original = termios.tcgetattr(descriptor)
    decoder = codecs.getincrementaldecoder(sys.stdin.encoding or 'utf-8')(errors='replace')
    selected, drawn, typed = 0, 0, ''
    try:
        tty.setcbreak(descriptor)
        sys.stdout.write('\033[?25l')
        while True:
            clear_rows(drawn)
            width = max(10, os.get_terminal_size(sys.stdout.fileno()).columns - 1)
            height = max(1, os.get_terminal_size(sys.stdout.fileno()).lines - 6)
            start = max(0, selected - height + 1)
            rows = [(label.upper(), '36')]
            rows += [(f"{'>' if i == selected else ' '} {i + 1}. {choices[i]}",
                      '1;36' if i == selected else None)
                     for i in range(start, min(len(choices), start + height))]
            hint = terminal.choice_hint(choices[selected])
            rows += [(hint or '', '2'), ('Up/Down: move | Enter: select | Ctrl+C: back', '2'),
                     ('Choice: ' + typed, None)]
            for text, style in rows:
                terminal.say(str(text)[:width], style)
            drawn = len(rows)
            byte = os.read(descriptor, 1)
            if not byte or byte == b'\x04':
                raise EOFError
            if byte == b'\x03':
                raise KeyboardInterrupt
            if byte == b'\x1b':
                sequence = b''
                for _ in range(2):
                    if not select.select([descriptor], [], [], 0.08)[0]:
                        break
                    sequence += os.read(descriptor, 1)
                if sequence in (b'[A', b'OA'):
                    selected = (selected - 1) % len(choices)
                elif sequence in (b'[B', b'OB'):
                    selected = (selected + 1) % len(choices)
                typed = ''
            elif byte in (b'\r', b'\n'):
                answer = typed.strip()
                if not answer:
                    return choices[selected]
                if answer in choices:
                    return answer
                if answer.isdigit() and 1 <= int(answer) <= len(choices):
                    return choices[int(answer) - 1]
                typed = ''
            elif byte in (b'\x7f', b'\x08'):
                typed = typed[:-1]
            else:
                character = decoder.decode(byte)
                if character.isprintable():
                    typed += character
    finally:
        # Discard buffered menu keys before returning to line input.
        termios.tcsetattr(descriptor, termios.TCSAFLUSH, original)
        clear_rows(drawn)
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()


class StageChecklist:
    def __init__(self, projects):
        self.steps = [('', 'analysis')]
        self.steps += [(p, s) for p in projects for s in STAGES if s not in ('analysis', 'heldout')]
        self.steps += [(p, 'heldout') for p in projects]
        self.states = {step: 'pending' for step in self.steps}
        self.current = None

    def advance(self, project, stage):
        step = (project, stage)
        if step not in self.states or step == self.current:
            return
        if self.current:
            self.states[self.current] = 'done'
        self.current = step
        self.states[step] = 'active'

    def finish(self, code):
        if self.current:
            self.states[self.current] = ('done' if code in (0, 3) else
                                         'cancelled' if code == 130 else 'failed')

    def rows(self):
        colors = dict(done='32', active='36', pending='2', failed='31', cancelled='33')
        return [(f"[{self.states[s]}] {STAGES[s[1]]}" + (f' / {s[0]}' if s[0] else ''),
                 colors[self.states[s]]) for s in self.steps]
