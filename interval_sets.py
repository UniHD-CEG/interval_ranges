#!/usr/bin/env python

###############################################################################
# Set library optimized for sets of integer intervals
#
# A "set" is a list containing any amount of sorted, non-overlapping,
# half-closed intervals. E.g. the python [(1, 3), (4, 5)] contains the
# elements 1, 2, and 4.
# The function coalesce can be used on unsorted sets with potentially
# overlapping intervals to sort them and coalesce overlapping and adjacent
# ranges.
###############################################################################

import unittest

def union(xs1, xs2):
    p1, p2 = 0, 0
    def lo1(): return xs1[p1][0] if p1 < len(xs1) else None
    def lo2(): return xs2[p2][0] if p2 < len(xs2) else None
    def hi1(): return xs1[p1][1] if p1 < len(xs1) else None
    def hi2(): return xs2[p2][1] if p2 < len(xs2) else None

    res = []

    while True:
        l1, l2 = lo1(), lo2()

        if l1 != None and l2 != None:
            if l1 < l2: start, end, p1 = l1, hi1(), p1+1
            else: start, end, p2 = l2, hi2(), p2+1
        elif l1 != None: start, end, p1 = l1, hi1(), p1+1
        elif l2 != None: start, end, p2 = l2, hi2(), p2+1
        else: break

        while True:
            l1, l2 = lo1(), lo2()
            if l1 != None and l1 <= end: end, p1 = max(end, hi1()), p1+1
            elif l2 != None and l2 <= end: end, p2 = max(end, hi2()), p2+1
            else: break

        res.append( (start, end) )
    return res

def intersect(xs1, xs2):
    p1, p2 = 0, 0
    def lo1(): return xs1[p1][0] if p1 < len(xs1) else None
    def lo2(): return xs2[p2][0] if p2 < len(xs2) else None
    def hi1(): return xs1[p1][1] if p1 < len(xs1) else None
    def hi2(): return xs2[p2][1] if p2 < len(xs2) else None
    res = []

    while lo1() != None and lo2() != None:
        lo = max(lo1(), lo2())
        hi = min(hi1(), hi2())
        if hi > lo:
            res.append( (lo, hi) )
        if hi1() < hi2():
            p1 += 1
        else:
            p2 += 1
    return res

def difference(xs1, xs2):
    p1, p2 = 0, 0
    def lo1(): return xs1[p1][0] if p1 < len(xs1) else None
    def lo2(): return xs2[p2][0] if p2 < len(xs2) else None
    def hi1(): return xs1[p1][1] if p1 < len(xs1) else None
    def hi2(): return xs2[p2][1] if p2 < len(xs2) else None
    res = []
    # processes one x1 in xs1
    while lo1() != None:
        while lo2() != None and hi2() < lo1(): p2 += 1
        if lo2() == None:
            res.append( (lo1(), hi1()) )
        elif lo2() > lo1():
            # maybe leading free space
            res.append( (lo1(), min(lo2(), hi1())) )
        start = None
        # processes all x2 in xs2 overlapping or contained in x1
        while lo2() != None and lo2() < hi1():
            if start != None:
                res.append( (start, min(lo2(), hi1())) )
                start = None
            if hi2() < hi1(): start = hi2()
            if hi2() < hi1():
                p2 += 1
            else:
                break
        if start != None:
            res.append( (start, hi1()) )
        p1 += 1
    return res


def coalesce(xs):
    if len(xs) == 0: return []
    xs = xs[:]
    xs.sort(key = lambda x: x[0])
    start, end = xs[0]
    res = []
    for x in xs[1:]:
        if x[0] <= end:
            end = max(end, x[1])
        else:
            res.append( (start, end) )
            start, end = x
    res.append( (start, end) )
    return res

def volume(xs):
    volume = 0
    for x in xs:
        volume += x[1] - x[0]
    return volume

class TestUnion(unittest.TestCase):
    def test_nooverlap(self):
        res = union([(1,2), (3,4)], [(5,6), (7,8)])
        self.assertEqual(res, [(1,2), (3,4), (5,6), (7,8)])
        res = union([(1,2), (5,6)], [(3,4), (7,8)])
        self.assertEqual(res, [(1,2), (3,4), (5,6), (7,8)])

    def test_consecutive(self):
        res = union([(1,2), (2,3)], [(4,5), (5,6)])
        self.assertEqual(res, [(1,3), (4,6)])
        res = union([(1,2), (4,5)], [(2,3), (5,6)])
        self.assertEqual(res, [(1,3), (4,6)])

    def test_noflipflop(self):
        res = union([(1,2), (2,4), (5,6)], [(6,7)])
        self.assertEqual(res, [(1,4), (5,7)])
        res = union([(1,2)], [(2,4), (5,6), (6,7)])
        self.assertEqual(res, [(1,4), (5,7)])

    def test_contained(self):
        res = union([(1,2), (3,6), (7,8)], [(4,5)])
        self.assertEqual(res, [(1,2), (3,6), (7,8)])
        res = union([(4,5)], [(1,2), (3,6), (7,8)])
        self.assertEqual(res, [(1,2), (3,6), (7,8)])

    def test_chained(self):
        res = union([(1,3), (4,7), (8,11)], [(2,5), (6,9), (10,13)])
        self.assertEqual(res, [(1,13)])

class TestCoalesce(unittest.TestCase):
    def test_empty(self):
        res = coalesce([])
        self.assertEqual(res, [])

    def test_nooverlap(self):
        res = coalesce([(1,2), (3,4), (5,6)])
        self.assertEqual(res, [(1,2), (3,4), (5,6)])

    def test_partial(self):
        res = coalesce([(1,3), (2,5), (4,6)])
        self.assertEqual(res, [(1,6)])

    def test_contained(self):
        res = coalesce([(1,7), (2,5), (8,10)])
        self.assertEqual(res, [(1,7), (8, 10)])

class TestIntersect(unittest.TestCase):
    def test_empty(self):
        res = intersect([], [])
        self.assertEqual(res, [])

    def test_single(self):
        res = intersect([(1, 5)], [(2,3)])
        self.assertEqual(res, [(2,3)])

        res = intersect([(1, 5)], [(5,6)])
        self.assertEqual(res, [])

        res = intersect([(1, 5)], [(4,6)])
        self.assertEqual(res, [(4,5)])

    def test_multiple(self):
        res = intersect([(1, 5)], [(1,3), (4,5)])
        self.assertEqual(res, [(1,3), (4,5)])

        res = intersect([(1, 5)], [(1,3), (4,7)])
        self.assertEqual(res, [(1,3), (4,5)])

        res = intersect([(1, 5), (6, 8)], [(1,5), (7,8)])
        self.assertEqual(res, [(1,5), (7,8)])

    def test_equal(self):
        res = intersect([(1, 3), (4, 6), (7, 9)], [(1, 3), (4, 6), (7, 9)])
        self.assertEqual(res, [(1, 3), (4, 6), (7, 9)])

class TestDifference(unittest.TestCase):
    def test_empty(self):
        res = difference([], [])
        self.assertEqual(res, [])

    def test_noB(self):
        res = difference([(1, 3)], [])
        self.assertEqual(res, [(1, 3)])

    def test_nooverlap(self):
        res = difference([(4, 9)], [(1, 3), (9, 10)])
        self.assertEqual(res, [(4, 9)])

    def test_contained(self):
        res = difference([(4, 9)], [(5, 6), (7, 8)])
        self.assertEqual(res, [(4, 5), (6, 7), (8, 9)])

    def test_overlap(self):
        res = difference([(4, 8)],
                            [(3, 5), (7, 9)])
        self.assertEqual(res, [(5, 7)])

        res = difference([(4, 8)],
                            [(1, 2), (3, 5), (7, 9)])
        self.assertEqual(res, [(5, 7)])

        res = difference([(4, 8), (9, 12)],
                            [(3, 5), (7, 10)])
        self.assertEqual(res, [(5, 7), (10, 12)])


if __name__ == "__main__":
    unittest.main()
