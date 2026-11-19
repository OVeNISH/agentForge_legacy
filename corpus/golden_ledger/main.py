

def split_bill(amount, people):
    return amount / people


def summarize(balances):
    total = 0
    for name, amount in balances.iteritems():
        total += amount
    return total


def parse_amount(text):
    try:
        return int(text)
    except ValueError, error:
        return 'invalid: ' + str(error)


if __name__ == '__main__':
    print 'split:', split_bill(7, 2), split_bill(-7, 2)
    print 'total:', summarize({'Ada': 7, 'Lin': -2})
    print 'empty:', summarize({})
    print 'parsed:', parse_amount('12')
    print 'bad:', parse_amount('bad')
