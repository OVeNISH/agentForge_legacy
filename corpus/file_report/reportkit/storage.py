"""Read numeric lines and serialize a report."""


def read_numbers(path):
    with open(path, 'rb') as stream:
        return [int(line.strip()) for line in stream if line.strip()]


def write_report(path, report):
    with open(path, 'wb') as stream:
        for key, value in sorted(report.iteritems()):
            stream.write('%s=%s\n' % (key, value))
