
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

    for i in xrange(len(s)):
        if chars_left == 0:
            # early exit
            return True

        cur_char = s[i]
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

        self.assertFalse(question1('pythonic', 'z'))
        self.assertFalse(question1('', 'abc'))
        self.assertFalse(question1('abcd', 'baa'))
        self.assertFalse(question1('abcd', 'bad'))
        self.assertFalse(question1('edddbit car', 'bad credit'))
        

###########################################################
# QUESTION 2
###########################################################
def question2(s):
    return ""


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


def question5(ll, m):
    return Node()



if __name__ == '__main__':
    unittest.main()
