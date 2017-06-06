
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
    # We are using Kruskal's algorithm to find the minimum spanning tree

    # order edges by weight
    edges = [(v1, v2, w) for v1, out_edges in G.iteritems() 
                         for v2, w in out_edges]
    edges.sort(key=lambda (v1, v2, w): w)
    
    # initial disjoint sets - each vertex in its own
    ds_index = range(len(G))
    vert_index = dict((v, i) for i, v in enumerate(G))

    def get_roots(v1, v2):
        idx1 = vert_index[v1]
        idx2 = vert_index[v2]
        while idx1 != ds_index[idx1]:
            idx1 = ds_index[idx1]
        while idx2 != ds_index[idx2]:
            idx2 = ds_index[idx2]
        return idx1, idx2

    # add edges, from lowest weight, joining the sets
    res_edges = []
    for edge in edges:
        v1, v2, _ = edge
        root1, root2 = get_roots(v1, v2)
        if root1 != root2:
            res_edges.append(edge)
            # "merge" the two disjoint sets
            ds_index[root1] = root2
        
    # convert to the output graph format
    res = dict((v, []) for v in G)
    for v1, v2, w in res_edges:
        res[v1].append((v2, w))
        res[v2].append((v1, w))

    return res


def order_graph(G):
    """Given a graph G, represented as a dictionary, orders edges by label name"""
    for _, edges in G.iteritems():
        edges.sort(key=lambda (v, w): v)
    return G

# QUESTION 3 TESTS
class Test3(unittest.TestCase):
    def test_base(self):
        G = {'A': [('B', 2)],
             'B': [('A', 2), ('C', 5)], 
             'C': [('B', 5)]}
        self.assertEquals(question3(G), G)
        
    def test_cc(self):
        G = {'A': [('B', 2)], 'B': [('A', 2)]}
        self.assertEquals(order_graph(question3(G)), G) 
        self.assertEquals(question3({}), {}) 

    def test_cc_disj(self):
        G = {'A': [('B', 2)], 'B': [('A', 2)], 
             'C': [('D', 2)], 'D': [('C', 2)]}
        self.assertEquals(order_graph(question3(G)), G) 

    def test_1(self):
        G = {'A': [('B', 2), ('C', 2)], 
             'B': [('A', 2), ('C', 3)], 
             'C': [('A', 2), ('B', 3)]}
        S = {'A': [('B', 2), ('C', 2)], 
             'B': [('A', 2)], 
             'C': [('A', 2)]}     
        self.assertEquals(order_graph(question3(G)), S) 
        

    def test_2(self):
        G = {'A': [('B', 1), ('C', 7)], 
             'B': [('A', 1), ('C', 5), ('D', 4), ('E', 3)], 
             'C': [('A', 7), ('B', 5), ('E', 6)],
             'D': [('B', 4), ('E', 2)], 
             'E': [('B', 3), ('C', 6), ('D', 2)]}
        S = {'A': [('B', 1)], 
             'B': [('A', 1), ('C', 5), ('E', 3)], 
             'C': [('B', 5)],
             'D': [('E', 2)], 
             'E': [('B', 3), ('D', 2)]} 
        self.assertEquals(order_graph(question3(G)), S)   

###########################################################
# QUESTION 4
###########################################################
def question4(T, r, n1, n2):
    n = len(T)
    if n1 >= n or n2 >= n or n1 < 0 or n2 < 0:
        return None

    def get_child(root, right):
        if right:
            r = xrange(root + 1, n)  
        else:
            r = xrange(root - 1, -1, -1)  
             
        for i in r:
            if T[root][i] == 1:
                return i
        return None

    def least_common_ancestor(root):
        if root > n1 and root > n2:
            return least_common_ancestor(get_child(root, False))
        elif root < n1 and root < n2:
            return least_common_ancestor(get_child(root, True))
        else:
            return root

    return least_common_ancestor(r)


# QUESTION 4 TESTS
class Test4(unittest.TestCase):
    def test(self):
        #    3
        #   0 4
        #  1

        self.assertEquals(question4(
            [[0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 0, 0, 0]], 3, 1, 4), 3)
        
        self.assertEquals(question4(
            [[0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0]], 3, 0, 5), None)

        #    4
        #   2
        #  1 3
        # 0
        self.assertEquals(question4(
            [[0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0],
             [0, 1, 0, 1, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0]], 4, 1, 4), 4)

        self.assertEquals(question4(
            [[0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0]], 4, 2, 4), 4)

        self.assertEquals(question4(
            [[0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0]], 4, 0, 3), 2)

        self.assertEquals(question4(
            [[0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0]], 4, 1, 3), 2)             

        self.assertEquals(question4(
            [[0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0]], 4, 2, 2), 2)
        
        self.assertEquals(question4(
            [[0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0]], 4, 0, 0), 0)

        self.assertEquals(question4(
            [[0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0]], 4, 0, 5), None)

###########################################################
# QUESTION 5
###########################################################
class Node(object):
  def __init__(self, data):
    self.data = data
    self.next = None

def get_list_length(node):
    res = 0
    while node is not None:
        node = node.next
        res += 1
    return res

def question5(ll, m):
    n = get_list_length(ll)
    if m < 1 or m > n:
        return None
    
    node = ll
    for k in xrange(n - m):
        node = node.next
    return node


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
        self.assertEquals(question5(make_list(5), 5).data, 1)
        self.assertEquals(question5(make_list(5), 6), None)
        self.assertEquals(question5(make_list(5), 0), None)
        self.assertEquals(question5(make_list(5), 1).data, 5)
        self.assertEquals(question5(make_list(1), 3), None)
        self.assertEquals(question5(make_list(1), 1).data, 1)
        self.assertEquals(question5(None, 10), None)


if __name__ == '__main__':
    unittest.main()
