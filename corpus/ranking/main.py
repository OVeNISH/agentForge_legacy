"""An in-memory scoreboard with an explicit comparison function."""


def compare_scores(left, right):
    score_order = cmp(right[1], left[1])
    if score_order:
        return score_order
    return cmp(left[0].lower(), right[0].lower())


class Scoreboard(object):
    def __init__(self):
        self.scores = {}

    def add(self, name, points):
        self.scores[name] = self.scores.get(name, 0) + points

    def ranked(self):
        rows = list(self.scores.iteritems())
        rows.sort(cmp=compare_scores)
        return rows


if __name__ == '__main__':
    board = Scoreboard()
    print 'empty:', repr(board.ranked())
    board.add('Lin', 4)
    board.add('ada', 7)
    board.add('Bob', 7)
    board.add('Lin', -1)
    print 'ranked:', repr(board.ranked())
    print 'equal:', compare_scores(('Ada', 7), ('Ada', 7))
