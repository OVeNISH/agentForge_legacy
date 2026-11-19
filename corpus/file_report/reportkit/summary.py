"""Keep Python 2 integer averaging visible in the report."""


def summarize(numbers):
    if not numbers:
        return {'count': 0, 'mean': None}
    return {'count': len(numbers), 'mean': sum(numbers) / len(numbers)}
