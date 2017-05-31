
import unittest

###########################################################
# QUESTION 1
###########################################################
def question1(s, t):
    char_reg = [0]*255
    
    # init character counts according to t
    for c in t:
        char_reg[ord(c)] += 1
    chars_left = len(t)

    anagram_start = 0

    for i, cur_char in enumerate(s):
        if chars_left == 0:
            # early exit
            return True

        idx = ord(cur_char)
        if char_reg[idx] > 0:
            # consume character from registry
            char_reg[idx] -= 1
            chars_left -= 1
        else:
            # can't consume, move the current anagram start
            while anagram_start <= i:
                start_char = s[anagram_start]
                anagram_start += 1
                if start_char == cur_char:
                    # we've just "freed" a character to consume
                    break
                char_reg[ord(start_char)] += 1
                chars_left += 1

    return chars_left == 0


# QUESTION 1 TESTS
class Test1(unittest.TestCase):
    def test(self):
        self.assertTrue(question1('', ''))
        self.assertTrue(question1('ab', ''))
        self.assertTrue(question1('abc', 'b'))
        self.assertTrue(question1('abcd', 'dcb'))
        self.assertTrue(question1('abbccd', 'cbcb'))
        self.assertTrue(question1('abcdbf', 'fdcb'))
        self.assertTrue(question1('abc', 'bca'))
        self.assertTrue(question1('udacity', 'ad'))
        self.assertTrue(question1('pythonic', 'noth'))
        self.assertTrue(question1('dddebit carddd', 'bad credit'))
        self.assertTrue(question1('deddbit carddd', 'bad credit'))
        self.assertTrue(question1('a'*100000, 'a'*100000))

        self.assertFalse(question1('pythonic', 'z'))
        self.assertFalse(question1('', 'abc'))
        self.assertFalse(question1('abcd', 'baa'))
        self.assertFalse(question1('abcd', 'bad'))
        self.assertFalse(question1('edddbit car', 'bad credit'))
        

###########################################################
# QUESTION 2
###########################################################
def question2(s):
    n = len(s)
    if n <= 1:
        return s

    def longest_palindrome_at(middle_pos, offs=0):
        """Returns the pair of furthest positions, (from, to), exclusive"""
        start = middle_pos
        end = min(middle_pos + offs, n - 1)
        while start >= 0 and end < n and s[start] == s[end]:
            start -= 1
            end += 1
        return (start, end)
    
    palindromes = (longest_palindrome_at(middle_pos, offs) 
                    for middle_pos in xrange(len(s)) 
                    for offs in [0, 1])
                    
    start, end = max(palindromes, key=lambda (s, e): e - s)
    return s[start + 1:end]


# QUESTION 2 TESTS
class Test2(unittest.TestCase):
    def test(self):
        self.assertEquals(question2(''), '')
        self.assertEquals(question2('a'), 'a')
        self.assertEquals(question2('aa'), 'aa')
        self.assertEquals(question2('ab'), 'a')
        self.assertEquals(question2('dabacb'), 'aba')
        self.assertEquals(question2('tdudacityticadutd'), 'udacityticadu')
        self.assertEquals(question2('daabbaaccb'), 'aabbaa')
        self.assertEquals(question2('udacity'), 'u')
        self.assertEquals(question2('udacity'), 'u')
        self.assertEquals(question2('uudacity'), 'uu')
        self.assertEquals(question2('uduacity'), 'udu')
        self.assertEquals(question2('a'*1000), 'a'*1000)


###########################################################
# QUESTION 3
###########################################################
def question3(G):
    return {}


###########################################################
# QUESTION 4
###########################################################
def question4(T, r, n1, n2):
    return 0


###########################################################
# QUESTION 5
###########################################################
class Node(object):
  def __init__(self, data):
    self.data = data
    self.next = None

from collections import deque

def question5(ll, m):
    d = deque()
    node = ll
    while node is not None:
        if len(d) >= m:
            d.popleft()
        d.append(node)
        node = node.next
    return d.popleft() if len(d) == m else None


# QUESTION 5 TESTS
class Test5(unittest.TestCase):
    def test(self):
        def make_list(n):
            head = Node(1)
            p = head
            for i in xrange(2, n + 1):
                node = Node(i)
                p.next = node
                p = node
            return head     

        self.assertEquals(question5(make_list(5), 3).data, 3)
        self.assertEquals(question5(make_list(1), 3), None)
        self.assertEquals(question5(make_list(1), 1).data, 1)
        self.assertEquals(question5(None, 10), None)


if __name__ == '__main__':
    unittest.main()
