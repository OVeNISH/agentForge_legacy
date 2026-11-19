"""Write a report in the current scratch directory."""

from reportkit import build_report


if __name__ == '__main__':
    print repr(build_report('sample.txt', 'report.txt', seed=7))
