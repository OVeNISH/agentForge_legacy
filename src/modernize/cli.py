"""Configuration, Python 2 analysis and guided terminal entry points."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

from modernize import __version__
from modernize.analysis import Python2Adapter, scan
from modernize.config import load_config
from modernize.logging import configure_logging


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="modernize", description="Legacy modernization CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--config", type=Path, help="JSON configuration file")
    commands = parser.add_subparsers(dest="command")
    commands.add_parser('tui', help='Launch the interactive guided terminal')
    commands.add_parser("config", help="Validate and print resolved configuration as JSON")
    scanning = commands.add_parser('scan', help='Analyze Python 2 source without executing it')
    scanning.add_argument('project', type=Path)
    scanning.add_argument('--analysis', choices=('sequential', 'parallel'), default='sequential')
    scanning.add_argument('--workers', type=int, choices=range(1, 5), default=2)
    scanning.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command is None:
        if sys.stdin.isatty():
            args.command = 'tui'
        else:
            parser.error('the following arguments are required: command')
    try:
        config = load_config(args.config)
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))
    if args.command == 'tui':
        from modernize.terminal import launch
        return launch(args.config)
    logger = configure_logging(config.log_level)
    logger.info("configuration_loaded")
    if args.command == 'scan':
        adapter = Python2Adapter(config.legacy_image, args.analysis, args.workers)
        record = dict(mode=args.analysis, workers=args.workers, status='failed')
        output = args.output.resolve()
        try:
            root = args.project.resolve(strict=True)
            if output == root or root in output.parents:
                raise ValueError('output must be outside the input project')
            output.mkdir(parents=True, exist_ok=False)
        except (OSError, ValueError) as error:
            parser.error(str(error))
        try:
            facts = scan(root, adapter)
            (output / 'facts.json').write_text(json.dumps(facts, sort_keys=True, indent=2) + '\n')
            record['status'] = 'passed'
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            record['error'] = str(error)
        record['image_id'] = getattr(adapter, 'image_id', None)
        record['parses'] = sorted(adapter.records, key=lambda r: r['path'])
        (output / 'run.json').write_text(json.dumps(record, sort_keys=True, indent=2) + '\n')
        if record['status'] != 'passed':
            parser.error(record['error'])
        logger.info('analysis_completed')
        print(json.dumps(dict(files=len(facts['files']), output=str(output / 'facts.json')), sort_keys=True))
        return 0
    print(json.dumps(config.to_dict(), sort_keys=True))
    return 0
