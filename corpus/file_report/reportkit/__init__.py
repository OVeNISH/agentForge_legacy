"""File reports exercise package imports and external state."""

import random
import time

from .storage import read_numbers, write_report
from .summary import summarize


def build_report(input_path, output_path, seed=None):
    with open(input_path, 'wb') as stream:
        stream.write('7\n-2\n0\n')
    numbers = read_numbers(input_path)
    report = summarize(numbers)
    report['ticket'] = random.Random(seed).randint(100, 999)
    report['created_at'] = time.time()
    write_report(output_path, report)
    return report
