"""Process text while retaining Python 2 list and encoding semantics."""


def clean_names(names):
    stripped = map(lambda name: name.strip(), names)
    return filter(None, stripped)


def pair_names(names):
    pairs = zip(range(len(names)), names)
    return len(pairs), pairs


def encode_label(label):
    return label.encode('utf-8')


def decode_label(raw):
    return raw.decode('utf-8')


def describe(raw):
    text = decode_label(raw)
    return type(raw).__name__, type(text).__name__, len(raw), len(text)


if __name__ == '__main__':
    names = clean_names([u' Ada ', u'', u' Lin '])
    print 'names:', repr(names)
    print 'pairs:', repr(pair_names(names))
    print 'empty:', repr(pair_names(clean_names([])))
    raw = encode_label(u'caf\u00e9')
    print 'encoded:', repr(raw)
    print 'decoded:', repr(decode_label(raw))
    print 'types:', repr(describe(raw))
