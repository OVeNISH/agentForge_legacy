"""Guided terminal commands over the existing CLI and repository workers."""

from datetime import datetime
import json
import os
from pathlib import Path
import pydoc
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import textwrap

from modernize import __version__
from modernize.terminal_widgets import STAGES, StageChecklist, arrow_choice, clear_rows, interactive

COMMANDS = {
    '/project': 'Choose a corpus project or a Python 2 folder',
    '/scan': 'Analyze the selected Python 2 folder',
    '/run': 'Run a registered corpus project or the whole corpus',
    '/review': 'Read a saved report, source, diffs or AST facts',
    '/verify': 'Verify a saved pipeline run offline',
    '/test': 'Run the tool unit and integration suites',
    '/status': 'Show selected project and latest output',
    '/menu': 'Open the numbered action menu',
    '/help': 'Show these commands',
    '/quit': 'Leave the terminal interface',
}

CHOICE_HINTS = {
    'custom Python 2 folder': 'Analyze your own code with /scan',
    'strict': 'Compare raw observations exactly (default)',
    'python2-python3.v1': 'Apply the documented runtime policy; keep raw results',
    'sequential': 'One parser at a time',
    'parallel': 'Use multiple bounded parser workers',
    'report': 'Results, coverage and unresolved cases',
    'facts': 'Browse the original code analysis',
}

def plain(text):
    # Artifact paths, source and worker errors may contain terminal control bytes.
    return re.sub(r'[\x00-\x08\x0b-\x1f\x7f-\x9f]', '', str(text))


def repository():
    # Never execute a lookalike scripts/ directory in an untrusted input project.
    path = Path(__file__).resolve().parents[2]
    if (path / 'scripts/run_pipeline.py').is_file() and (path / 'corpus/manifest.json').is_file():
        return path
    return None


class Terminal:
    def __init__(self, config_path=None):
        self.root = repository()
        self.config_path = config_path.resolve() if config_path else None
        self.projects = {}
        if self.root:
            manifest = json.loads((self.root / 'corpus/manifest.json').read_text())
            for entry in manifest['projects']:
                name = entry['id']
                if not isinstance(name, str) or not re.fullmatch(r'[\w-]+', name) or name in self.projects:
                    raise ValueError('invalid or duplicate corpus project ID')
                self.projects[name] = (self.root / 'corpus' / name).resolve()
        self.project = next(iter(self.projects.values()), Path.cwd())
        self.output = None
        self.color = sys.stdout.isatty() and os.environ.get('TERM') != 'dumb' and 'NO_COLOR' not in os.environ

    def say(self, text='', style=None):
        text = plain(text)
        if self.color and style:
            text = '\033[' + style + 'm' + text + '\033[0m'
        print(text, flush=True)

    def ask(self, label, default=None):
        self.say('\n  ' + label, '1')
        if default is not None:
            self.say('  Enter to use: ' + str(default), '2')
        answer = input('  > ').strip()
        return answer or (str(default) if default is not None else '')

    def panel(self, title, lines):
        width = max(12, min(shutil.get_terminal_size().columns, 88)) - 4
        self.say('\n  +' + '-' * (width - 2) + '+', '36')
        for line in [title, '', *lines]:
            for wrapped in textwrap.wrap(plain(line), width=width - 4) or ['']:
                self.say('  | ' + wrapped.ljust(width - 4) + ' |', '1;36' if line == title else None)
        self.say('  +' + '-' * (width - 2) + '+', '36')

    def choose(self, label, choices):
        if interactive():
            answer = arrow_choice(self, label, choices)
            self.say(f'  {label}: {answer}', '36')
            return answer
        self.say('\n  ' + label.upper(), '1;36')
        for index, choice in enumerate(choices, 1):
            self.say(f'  {index}. {choice}', '1' if index == 1 else None)
            hint = self.choice_hint(choice)
            if hint:
                self.say('     ' + hint, '2')
        while True:
            answer = self.ask(label, '1')
            if answer in choices:
                return answer
            if answer.isdigit() and 1 <= int(answer) <= len(choices):
                return choices[int(answer) - 1]
            self.say('Choose a listed number or name.', '31')

    def choice_hint(self, choice):
        return COMMANDS.get(choice) or CHOICE_HINTS.get(choice)

    def folder(self, text):
        path = Path(text).expanduser().resolve(strict=True)
        if not path.is_dir():
            raise ValueError('Choose a directory: ' + str(path))
        return path

    def project_command(self, path=None):
        if path is None:
            choice = self.choose('Project', [*self.projects, 'custom Python 2 folder'])
            path = self.projects.get(choice)
            if path is None:
                path = self.ask('Folder path', self.project)
        elif path in self.projects:
            path = self.projects[path]
        self.project = self.folder(path)
        self.status()

    def status(self):
        self.say(f'\n  MODERNIZE {__version__} | Guided terminal | YOUR WORKSPACE', '1;36')
        for line in ('Project: ' + str(self.project), 'Output: ' + str(self.output or 'none selected')):
            for row in textwrap.wrap(line, width=max(10, shutil.get_terminal_size().columns - 4)):
                self.say('  ' + row)
        if not self.root:
            self.say('  Repository unavailable: scanning only.', '33')

    def output_folder(self, prefix, source=None):
        base = self.root / 'artifacts' if self.root else Path(tempfile.gettempdir()) / 'modernize-runs'
        if source and (base == source or source in base.parents):
            base = Path(tempfile.gettempdir()) / 'modernize-runs'
        default = base / (prefix + '-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
        while True:
            path = Path(self.ask('New output folder', default)).expanduser().resolve()
            if path.exists():
                self.say('That path already exists. Choose a new output folder.', '31')
            elif source and (path == source or source in path.parents):
                self.say('Output must be outside the input project.', '31')
            else:
                return path

    def analysis_options(self):
        mode = self.choose('Analysis', ['sequential', 'parallel'])
        options = ['--analysis', mode]
        if mode == 'parallel':
            options += ['--workers', self.choose('Workers', ['1', '2', '3', '4'])]
        return options

    def config_options(self):
        return ['--config', str(self.config_path)] if self.config_path else []

    def script(self, name):
        if self.root is None:
            raise ValueError('Launch from the repository checkout to use pipeline, verification and test commands.')
        return [sys.executable, '-u', str(self.root / 'scripts' / name)]

    def event(self, value):
        if isinstance(value, dict) and isinstance(value.get('totals'), dict):
            status = str(value.get('status', 'unknown'))
            self.say('Recorded status: ' + status,
                     '32' if status == 'passed' else '31' if status == 'failed' else '33')
            raw = value['totals'].get('converted_on_modern')
            if raw:
                self.say(f"Raw converted: {raw['passed']}/{raw['tests']}")
        elif isinstance(value, dict) and isinstance(value.get('policy'), dict):
            policy = value['policy']
            self.say(f"Policy {policy.get('name', '')}: {policy.get('passed', '?')}/{policy.get('tests', '?')}; "
                     f"held-out {policy.get('heldout_passed', '?')}/{policy.get('heldout_tests', '?')}")
        elif isinstance(value, dict) and 'message' in value:
            self.say('  ' + str(value['message']))
        elif isinstance(value, dict) and 'files' in value and 'output' in value:
            self.say(f"Scanned {value['files']} Python files. Facts: {value['output']}")
        else:
            self.say(json.dumps(value, indent=2))

    def job(self, command):
        self.say('\n[Running] Ctrl+C requests cancellation and waits for cleanup.', '36')
        checklist = None
        if any(Path(str(p)).name == 'run_pipeline.py' for p in command) and '--output' in command:
            scope = command[command.index('--project') + 1] if '--project' in command else 'all'
            checklist = StageChecklist(list(self.projects) if scope == 'all' else [scope])
        drawn = 0

        def clear_checklist():
            nonlocal drawn
            if drawn:
                clear_rows(drawn)
                drawn = 0

        def draw_checklist():
            nonlocal drawn
            clear_checklist()
            rows = checklist.rows()
            if interactive():
                height = max(1, shutil.get_terminal_size().lines - 5)
                active = next((i for i, s in enumerate(checklist.steps) if s == checklist.current), 0)
                start = max(0, active - height + 1)
                rows = rows[start:start + height]
            width = max(10, shutil.get_terminal_size().columns - 1)
            for text, style in rows:
                self.say(text[:width] if interactive() else text, style)
            drawn = len(rows) if interactive() else 0

        environment = dict(os.environ, PYTHONUNBUFFERED='1')
        if self.root:
            environment['PYTHONPATH'] = str(self.root / 'src') + os.pathsep + environment.get('PYTHONPATH', '')
        cancelled = False
        pending = ''
        with subprocess.Popen(command, cwd=self.root or Path.cwd(), env=environment,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                              errors='replace', start_new_session=True) as process:
            while True:
                try:
                    for line in process.stdout:
                        clear_checklist()
                        if pending or line.lstrip().startswith('{'):
                            pending += line
                            try:
                                event = json.loads(pending)
                            except ValueError:
                                if len(pending) < 16384:
                                    continue
                                self.say(pending.rstrip('\n'))
                            else:
                                self.event(event)
                            pending = ''
                            continue
                        message = line.strip()
                        project, separator, stage = message.rpartition(':')
                        if message == 'analysis' or (separator and stage in STAGES):
                            stage = stage if separator else message
                            if checklist:
                                checklist.advance(project if separator else '', stage)
                                draw_checklist()
                            else:
                                self.say('\n  [Stage] ' + STAGES[stage] + (f' / {project}' if separator else ''), '1;36')
                        else:
                            self.say('  ' + line.rstrip('\n'))
                    code = process.wait()
                    break
                except KeyboardInterrupt:
                    clear_checklist()
                    if not cancelled:
                        cancelled = True
                        self.say('Cancellation requested; allowing worker cleanup.', '33')
                        # Signal the controller only, so its Docker cleanup subprocess can finish.
                        try:
                            process.send_signal(signal.SIGINT)
                        except ProcessLookupError:
                            pass
        if pending:
            self.say(pending.rstrip('\n'))
        if checklist:
            checklist.finish(130 if cancelled else code)
            draw_checklist()
        if cancelled:
            self.say('Cancelled. Partial artifacts may remain.', '33')
            return 130
        messages = {0: 'Command completed.', 1: 'Checks failed or compared rates differ.',
                    2: 'Input, setup or stage error.', 3: 'Run completed with unresolved cases or review flags.'}
        self.say(messages.get(code, 'Worker failed.') + f' Exit {code}.',
                 '32' if code == 0 else '33' if code == 3 else '31')
        return code

    def scan_command(self, path=None):
        project = self.folder(path) if path else self.project
        output = self.output_folder('scan', project)
        # An installed wheel must not import a shadow package from an untrusted cwd.
        flags = ['-u'] if self.root else ['-u', '-I']
        command = [sys.executable, *flags, '-m', 'modernize', *self.config_options(),
                   'scan', str(project), '--output', str(output), *self.analysis_options()]
        code = self.job(command)
        if (output / 'run.json').is_file():
            self.output = output
        if code == 0:
            self.say('Facts saved. Use /review to inspect them.', '32')

    def run_command(self):
        while True:
            output = self.run_once()
            if output is None or not interactive() or not self.next_actions(output):
                break

    def run_once(self):
        command = self.script('run_pipeline.py')
        name = next((n for n, p in self.projects.items() if p == self.project), None)
        if name is None:
            raise ValueError('Full runs support registered corpus projects. Use /project to select one; /scan accepts custom Python 2 folders.')
        scope = self.choose('Run scope', [name, 'all'])
        self.say('Strict compares raw observations. The explicit policy retains raw results and separately compares Python 2/3 representations.')
        comparison = self.choose('Comparison', ['strict', 'python2-python3.v1'])
        output = self.output_folder('run', self.project)
        code = self.job(command + self.config_options() + ['--project', scope, '--comparison', comparison,
                        '--output', str(output), *self.analysis_options()])
        if (output / 'run.json').is_file():
            self.output = output
        if code in (0, 3) and (output / 'report.json').is_file():
            self.summary(output)
            return output
        self.say('Use /review for reports and diffs; /verify checks the saved evidence.')

    def next_actions(self, output):
        while True:
            action = self.choose('Next action', ['View report', 'Inspect changes', 'Verify',
                                               'Run again', 'Return to prompt'])
            if action == 'Run again':
                return True
            if action == 'Return to prompt':
                return False
            if action == 'Verify':
                self.job(self.script('run_pipeline.py') + ['--verify', str(output)])
            else:
                self.review_command(str(output), choice='report' if action == 'View report' else 'diffs')

    def summary(self, output):
        report = json.loads((output / 'report.json').read_text())
        self.say('\nRecorded results (run /verify to check the saved evidence)', '1')
        mode = report.get('comparison', 'strict')
        if mode not in ('strict', 'python2-python3.v1'):
            mode = report.get('policy', {}).get('name', 'strict')
        self.say('  Comparison mode: ' + mode, '1;36')
        for project in report['projects']:
            raw = project['rates']['converted_on_modern']
            policy = project.get('policy')
            fraction = lambda v: f"{v['passed']}/{v['tests']}" if v else '-'
            self.say('\n  ' + project['project'], '1;36')
            for label, value in [('Raw matches', raw), ('Policy passes', policy),
                                 ('Held-out raw', project.get('heldout')),
                                 ('Held-out policy', policy.get('heldout') if policy else None)]:
                self.say(f'  {label:<18} {fraction(value)}',
                         '32' if value and value['passed'] == value['tests'] else '33')
        self.say('  Raw = exact observations. Policy = selected runtime comparison.', '2')
        self.say('  A dash means no policy result was recorded.', '2')
        self.say('Report: ' + str(output / 'report.md'))

    def select_output(self, path=None):
        output = self.folder(path or self.ask('Saved output folder', self.output))
        if not any((output / p).is_file() for p in ('run.json', 'report.json', 'facts.json')):
            raise ValueError('Choose a scan or pipeline output folder.')
        self.output = output
        return output

    def review_command(self, path=None, choice=None):
        output = self.select_output(path)
        choice = choice or self.choose('Review', ['report', 'diffs', 'source', 'facts'])
        if choice in ('report', 'facts'):
            paths = [output / ('report.md' if choice == 'report' else 'facts.json')]
        else:
            pattern = '*/diffs/**/*.diff' if choice == 'diffs' else '*/repair/source/**/*.py'
            paths = sorted(output.glob(pattern))
        paths = [p for p in paths if p.is_file() and p.resolve().is_relative_to(output)]
        if not paths:
            raise ValueError('No saved ' + choice + ' files in this output.')
        names = [str(p.relative_to(output)) for p in paths]
        selected = names[0] if len(names) == 1 else self.choose('File', names)
        with (output / selected).open(encoding='utf-8', errors='replace') as stream:
            text = stream.read(1024 * 1024 + 1)
        if len(text) > 1024 * 1024:
            text = text[:1024 * 1024] + '\n[Preview truncated at 1 MiB; read the full artifact in an editor.]'
        self.say('[Review] Viewing ' + selected + '. Press q to return from the pager.', '33')
        pydoc.pager(plain(text))

    def dispatch(self, line):
        parts = shlex.split(line)
        if not parts:
            return self.dispatch('/menu')
        command, *args = parts
        if command not in COMMANDS:
            raise ValueError('Unknown command. Use /help to see guided commands.')
        if len(args) > 1 or (args and command not in ('/project', '/scan', '/review', '/verify')):
            raise ValueError('This command accepts ' + ('one quoted path.' if command in ('/project','/scan','/review','/verify') else 'no arguments.'))
        path = args[0] if args else None
        if command == '/quit':
            return False
        if command == '/menu':
            return self.dispatch(self.choose('What would you like to do?', [c for c in COMMANDS if c != '/menu']))
        if command == '/help':
            for title, commands in [('START', ('/project', '/scan', '/run')),
                                    ('EXPLORE RESULTS', ('/review', '/verify')),
                                    ('SESSION', ('/status', '/test', '/menu', '/help', '/quit'))]:
                self.say('\n  ' + title, '1;36')
                for name in commands:
                    self.say(f'  {name:<10} {COMMANDS[name]}')
            self.say('Paths with spaces can be entered at prompts or quoted after a command. Ctrl+D exits; Ctrl+C cancels a prompt.')
        elif command == '/status':
            self.status()
        elif command == '/project':
            self.project_command(path)
        elif command == '/scan':
            self.scan_command(path)
        elif command == '/run':
            self.run_command()
        elif command == '/review':
            self.review_command(path)
        elif command == '/verify':
            output = self.select_output(path)
            if not (output / 'report.json').is_file():
                raise ValueError('/verify requires a pipeline output; scan metadata is available through /review.')
            self.job(self.script('run_pipeline.py') + ['--verify', str(output)])
        elif command == '/test':
            self.job(self.script('test.py'))
        return True

    def run(self):
        try:
            import readline  # noqa: F401 -- in-memory input history/editing on supported terminals.
        except ImportError:
            pass
        self.status()
        self.say('\n  QUICK START  /project  /scan  /run  |  /help for all commands', '36')
        self.say('  Enter: action menu | Up/Down: move | Ctrl+C: cancel | Ctrl+D: quit', '2')
        self.say()
        while True:
            try:
                if not self.dispatch(input('modernize> ')):
                    break
            except EOFError:
                break
            except KeyboardInterrupt:
                self.say('\nInput cancelled. /quit exits.', '33')
            except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
                self.say('Error: ' + str(error), '31')
        self.say('\nSession closed. Saved artifacts remain available.')
        return 0


def launch(config_path=None):
    try:
        return Terminal(config_path).run()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('Terminal setup error: ' + plain(error), file=sys.stderr)
        return 2
