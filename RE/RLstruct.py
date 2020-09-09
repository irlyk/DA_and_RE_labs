class Regex(object):
    def __init__(self, empty):
        self.empty = empty
        self.marked = False

    def reset(self):
        self.marked = False

    def shift(self, c, mark):
        marked = self._shift(c, mark)
        self.marked = marked
        return marked

    def __str__(self):
        return object.__str__()


def match(re, s):
    if not s:
        return re.empty
    result = re.shift(s[0], True)
    for c in s[1:]:
        result = re.shift(c, False)
    re.reset()
    return result


class Char(Regex):
    def __init__(self, c):
        Regex.__init__(self, False)
        self.c = c

    def _shift(self, c, mark):
        return mark and (c == self.c)

    def __str__(self):
        return self.c


class Epsilon(Regex):
    def __init__(self):
        Regex.__init__(self, empty=True)

    def _shift(self, c, mark):
        return False


class Binary(Regex):
    def __init__(self, left, right, empty):
        Regex.__init__(self, empty)
        self.left = left
        self.right = right

    def reset(self):
        self.left.reset()
        self.right.reset()
        Regex.reset(self)


class Alternative(Binary):  ## +
    def __init__(self, left, right):
        empty = left.empty or right.empty
        Binary.__init__(self, left, right, empty)

    def _shift(self, c, mark):
        marked_left = self.left.shift(c, mark)
        marked_right = self.right.shift(c, mark)
        return marked_left or marked_right

    def __str__(self):
        return self.left.__str__() + " + " + self.right.__str__()


class Sequence(Binary):
    def __init__(self, left, right):
        empty = left.empty and right.empty
        Binary.__init__(self, left, right, empty)

    def _shift(self, c, mark):
        old_marked_left = self.left.marked
        marked_left = self.left.shift(c, mark)
        marked_right = self.right.shift(
            c, old_marked_left or (mark and self.left.empty))
        return (marked_left and self.right.empty) or marked_right

    def __str__(self):
        return self.left.__str__() + "." + self.right.__str__()


class Repetition(Regex):  # *
    def __init__(self, re):
        Regex.__init__(self, True)
        self.re = re

    def _shift(self, c, mark):
        return self.re.shift(c, mark or self.marked)

    def reset(self):
        self.re.reset()
        Regex.reset(self)

    def __str__(self):
        return "(" + self.re.__str__() + ")*"


if __name__ == '__main__':
    o = Char('0')
    l = Char('1')
    re1 = Sequence(l, o)  # 1.0
    re2 = Sequence(o, Repetition(re1))  # 0.(1.0)*
    #re_test = Alternative(Char('0'), Repetition(Sequence(Char('0'), Char('1'))))  # (0 + (0.1)*)



    rel = Sequence(Char('0'), Repetition(Sequence(Char('1'), Char('0'))))  # 0.(1.0)*
    s = "01010"
    print(match(re2, s))



    print("rel:", match(rel, s))
    #print("re_test:", match(re_test, s))
    # # (a + b + c)* abcbac
    # re = RL.Repetition(RL.Alternative(RL.Alternative(RL.Char('a'), RL.Char('b')), RL.Char('c')))
    # s = 'abcbac'
    # print(RL.match(re, s))
