import unittest
from main import Earley


class Test1(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        d = dict()
        d['notterms'], d['terms'], d['rule'] = 1, 2, 2
        d['neterms'] = 'T'
        d['alphabet'] = 'ab'
        d['rules'] = ['T->aTbT', 'T->']
        d['start_symbol'] = 'T'
        self.earley.entry(d)

    def runTest(self):
        expected = [("aababb", True), ("aabbba", False), ("abbab", False), ("aaababbb", True), ("abba", False), ("ab", True), ("", True)]
        for string, result in expected:
            self.assertEqual(self.earley.answer(string), result)


class Test2(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        d = dict()
        d['notterms'], d['terms'], d['rule'] = 3, 4, 8
        d['neterms'] = 'SMT'
        d['alphabet'] = 'abcdpm'
        d['rules'] = ['S->SpM', 'S->M', 'M->MmT', 'M->T', 'T->a', 'T->b', 'T->c', 'T->d']
        d['start_symbol'] = 'S'
        self.earley.entry(d)

    def runTest(self):
        expected = [
            ("apbmd", True),
            ("apbmcpd", True),
            ("apd", True),
            ("a", True),
            ("apmd", False),
            ("dp", False),
            ("p", False),
            ("zzzzzzzzz", False),
        ]
        for string, result in expected:
            self.assertEqual(self.earley.answer(string), result)


class Test3(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        d = dict()
        d['notterms'], d['terms'], d['rule'] = 4, 2, 5
        d['neterms'] = 'SABQ'
        d['alphabet'] = 'aw'
        d['rules'] = ['S->aSS', 'S->SA', 'A->Aa', 'A->BAw', 'Q->']
        d['start_symbol'] = 'S'
        self.earley.entry(d)

    def runTest(self):
        expected = [("aaaaa", False), ("awa", False), ("", False), ("a", False)]
        for string, result in expected:
            self.assertEqual(self.earley.answer(string), result)


class Test4(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        d = dict()
        d['notterms'], d['terms'], d['rule'] = 3, 3, 5
        d['neterms'] = 'SABQ'
        d['alphabet'] = 'abc'
        d['rules'] = ['S->aAbB', 'A->cA', 'B->ccB', 'A->', 'B->']
        d['start_symbol'] = 'S'
        self.earley.entry(d)

    def runTest(self):
        expected = [("acbcc", True), ("acccbccc", False), ("acbc", False), ("accccbcccccc", True)]
        for string, result in expected:
            self.assertEqual(self.earley.answer(string), result)


class Test5(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        d = dict()
        d['notterms'], d['terms'], d['rule'] = 4, 3, 8
        d['neterms'] = 'STUV'
        d['alphabet'] = 'abc'
        d['rules'] = ['S->aTc', 'S->cS', 'T->aU', 'T->aT', 'U->aU', 'U->V', 'V->bV', 'V->c']
        d['start_symbol'] = 'S'
        self.earley.entry(d)

    def runTest(self):
        expected = [("caaacc", True), ("aacc", True), ("cccacc", False), ("aabbbbcc", True)]
        for string, result in expected:
            self.assertEqual(self.earley.answer(string), result)


class Test6(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        d = dict()
        d['notterms'], d['terms'], d['rule'] = 3, 3, 6
        d['neterms'] = 'STU'
        d['alphabet'] = 'abc'
        d['rules'] = ['S->bT',
                      'S->a',
                      'T->cUac',
                      'T->',
                      'U->bSab',
                      'U->a']
        d['start_symbol'] = 'S'
        self.earley.entry(d)

    def runTest(self):
        expected = [("bcbaabac", True), ("bcbcabac", False), ("bcbac", False), ("a", True)]
        for string, result in expected:
            self.assertEqual(self.earley.answer(string), result)


class Test7(unittest.TestCase):
    earley = Earley()

    def setUp(self):
        d = dict()
        d['notterms'], d['terms'], d['rule'] = 3, 2, 6
        d['neterms'] = 'STU'
        d['alphabet'] = 'bc'
        d['rules'] = ['S->SbSb', 'S->Tb', 'S->bS', 'S->cU', 'T->Ub', 'U->']
        d['start_symbol'] = 'S'
        self.earley.entry(d)

    def runTest(self):
        expected = [("bbbcb", True), ("bbbbbbbbcc", False), ("bbbbbbbbbbbbbbbbcbcbcbb", True),("bbbbbbbbbbbbbb", True)]
        for string, result in expected:
            self.assertEqual(self.earley.answer(string), result)



if __name__ == '__main__':
    unittest.main()
