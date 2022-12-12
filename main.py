class Earley:

    class Point:
        neterminal_from = 0
        left = []
        right = []
        k = 0


        def __init__(self):
            self.neterminal_from = 0
            self.left = []
            self.right = []
            self.k = 0


        def __eq__(self, other):
            return (self.k == other.k) and (self.right == other.right) and (self.left == other.left) and (self.neterminal_from == other.neterminal_from)


    def __init__(self):
        self.P = dict()
        self.comparison = dict()
        self.states = []
        self.alpha = []    
        self.nonterminal = ['S1']
        self.start = ''


    def entry(self, d):
        n = d['notterms']
        e = d['terms']
        p = d['rule']
        self.comparison['S1'] = 0
        for k in range(n):
            symb = d['neterms'][k]
            if symb in self.nonterminal:
                continue
            self.comparison[symb] = k + 1
            self.nonterminal.append(symb)
            self.P[symb] = []
        alphabet = d['alphabet']
        for elem in alphabet:
            self.alpha.append(elem)
        for k in range(p):
            rule = d['rules'][k]
            arr = rule.split('->')
            arr_right_part = []
            for elem in arr[1]:
                if elem in self.nonterminal:
                    arr_right_part.append(['nonterminal', self.nonterminal.index(elem)])
                else:
                    arr_right_part.append(['alpha', self.alpha.index(elem)])
            self.P[arr[0]].append(arr_right_part)
        self.start = d['start_symbol']
        return 0

    def scan(self, j, word):
        if j >= len(word):
            return
        a = word[j]
        if a not in self.states[j]:
            return
        for st in self.states[j][a]:
            new_st = self.Point()
            new_st.right = st.right.copy()
            new_st.left = st.left.copy()
            new_st.k = st.k
            new_st.neterminal_from = st.neterminal_from
            if not new_st.right:
                if new_st not in self.states[j + 1]['$']:
                    self.states[j + 1]['$'].append(new_st)
                continue
            new_st.left.append(new_st.right[0])
            new_st.right.pop(0)
            if not new_st.right:
                if new_st not in self.states[j + 1]['$']:
                    self.states[j + 1]['$'].append(new_st)
                continue
            first_symb_after_dot = new_st.right[0].copy()
            if first_symb_after_dot[0] == 'nonterminal':
                first_symb_after_dot = self.nonterminal[first_symb_after_dot[1]]
            else:
                first_symb_after_dot = self.alpha[first_symb_after_dot[1]]
            if st in self.states[j + 1][first_symb_after_dot]:
                continue
            self.states[j + 1][first_symb_after_dot].append(new_st)


    def complete(self, j, word):
        for st in self.states[j]['$']:
            k = st.k
            neterm = st.neterminal_from
            if self.nonterminal[neterm] not in self.states[k]:
                continue
            for rule in self.states[k][self.nonterminal[neterm]]:
                new_st = self.Point()
                new_st.right = rule.right.copy()
                new_st.left = rule.left.copy()
                new_st.k = rule.k
                new_st.neterminal_from = rule.neterminal_from
                if not new_st.right:
                    if new_st not in self.states[j]['$']:
                        self.states[j]['$'].append(new_st)
                    continue
                new_st.left.append(new_st.right[0])
                new_st.right.pop(0)
                if not new_st.right:
                    if new_st not in self.states[j]['$']:
                        self.states[j]['$'].append(new_st)
                    continue
                if new_st.right[0][0] == 'nonterminal':
                    first_symb_after_dot = self.nonterminal[new_st.right[0][1]]
                else:
                    first_symb_after_dot = self.alpha[new_st.right[0][1]]
                if new_st in self.states[j][first_symb_after_dot]:
                    continue
                self.states[j][first_symb_after_dot].append(new_st)


    def predict(self, j, word):
        for neterm in self.nonterminal:
            if neterm not in self.P:
                continue
            for rule in self.P[neterm]:
                new_st = self.Point()
                new_st.neterminal_from = self.comparison[neterm]
                new_st.k = j
                new_st.left = []
                new_st.right = rule.copy()
                if not new_st.right:
                    if new_st not in self.states[j]['$']:
                        self.states[j]['$'].append(new_st)
                    continue
                if new_st.right[0][0] == 'nonterminal':
                    first_symb_after_dot = self.nonterminal[new_st.right[0][1]]
                else:
                    first_symb_after_dot = self.alpha[new_st.right[0][1]]
                if first_symb_after_dot not in self.states[j]:
                    self.states[j][first_symb_after_dot] = []
                fl = 0
                for elem in self.states[j][first_symb_after_dot]:
                    if new_st == elem:
                        fl = 1
                        break
                if fl:
                    continue
                self.states[j][first_symb_after_dot].append(new_st)


    def answer(self, word):
        for symb in word:
            if symb not in self.alpha:
                return False
        self.states = [None] * (len(word) + 1)
        for k in range(len(word) + 1):
            self.states[k] = dict()
        first = self.Point()
        first.neterminal_from = 0
        first.k = 0
        first.left = []
        first.right = [['nonterminal', self.comparison[self.start]]]
        self.states[0][self.start] = [first]
        self.states[0]['S1'] = []
        for i in range(1, len(word) + 1):
            for a in self.alpha:
                self.states[i][a] = []
            for a in self.nonterminal:
                self.states[i][a] = []
            self.states[i]['$'] = []
        self.states[0]['$'] = []
        temp = self.states[0].copy()
        self.predict(0, word)
        self.complete(0, word)
        while temp != self.states[0]:
            temp = self.states[0].copy()
            self.predict(0, word)
            self.complete(0, word)

        for j in range(1, len(word) + 1):
            self.scan(j - 1, word)
            while self.states[j] != temp:
                temp = self.states[j].copy()
                self.predict(j, word)
                self.complete(j, word)
        last_st = self.Point()
        last_st.right = []
        last_st.left = [['nonterminal', self.comparison[self.start]]]
        last_st.neterminal_from = 0
        last_st.k = 0
        for elem in self.states[len(word)]['$']:
            if (last_st.k == elem.k) and (last_st.right == elem.right) and (last_st.left == elem.left) and (last_st.neterminal_from == elem.neterminal_from):
                return True
        return False


def insertion(d):
    for i in range(d['rule']):
        d['rules'].append(input())
    d['notterms'], d['terms'], d['rule'] = map(int, input().split())
    d['neterms'] = input()
    d['alphabet'] = input()
    d['rules'] = []
    d['start_symbol'] = input()


def main():
    t = Earley()
    d = dict()
    insertion(d)
    t.entry(d)
    x = int(input())
    for i in range(x):
        word = input()
        if t.answer(word):
            print("YES")
        else:
            print("NO")

if __name__ == '__main__':
    main()
