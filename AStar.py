__author__ = 'Douglas Lewis @ douglasdlewis2012@gmail.com'

from collections import defaultdict
from heapq import heappop, heappush
from timeit import timeit
import random
import cProfile as profile
'''
Given two five letter words, A and B, and a dictionary of five letter words,
find a shortest transformation from A to B, such that only one letter can be
changed at a time and all intermediate words in the transformation must exist in the dictionary.
 
For example, if A and B are "smart" and "brain", the result may be:
smart
    start
    stark
    stack
    slack
    black
    blank
    bland
    brand
    braid
brain
 
Your implementation should take advantage of multiple CPU cores.
Please also include test cases against your algorithm.
Your solution should produce the words that make up the shortest path itself, not just the count.
'''

class AStar:

    def __init__(self):
        print('initializing')

    class Node:

        def __init__(self, f, g, word, previous):
            self.f = f
            self.g = g
            self.word = word
            self.previous = previous

        def __lt__(self, other):
            return self.f < other.f

    def heuristic(self,word, end):
        return sum([a != b for a,b in zip(word,end)])

    def generate_neighbors(self, words):
        holder = object()
        match = defaultdict(list)
        neighbors = defaultdict(list)
        for w in words:
            for i in range(len(w)):
                p = tuple(holder if i == j else c for j, c in enumerate(w))
                m = match[p]
                m.append(w)
                neighbors[w].append(m)
        return neighbors

    def reconstruct_path(self, node):
        path = [node.word]
        while node.previous != None:
            temp = node.previous
            node = node.previous
            path.append(temp.word)
        p = path[::-1]

        return ' '.join(p)


    def a_star_search(self, start, end, words):
        neighbors = self.generate_neighbors(words)
        openSet = set([start])
        closedSet = set()
        heap = [AStar.Node(self.heuristic(start, end),0,start, None)]

        while len(heap) > 0:
            node = heappop(heap)
            if node.word == end:
                return self.reconstruct_path(node)

            openSet.remove(node.word)
            closedSet.add(node.word)

            g = node.g + 1
            for n in neighbors[node.word]:
                for w in n:
                    if w in closedSet:
                        continue

                    if w not in openSet:
                        new_node = AStar.Node(self.heuristic(w, end) + g, g, w, node)
                        heappush(heap, new_node)
                        openSet.add(w)

        msg = 'No way found! between %s - %s' %(start, end)
        return msg

    def get_words(self, size=5):
        all_words = [w.strip().lower() for w in open('words.txt')]

        print('total words: ' , len(all_words))
        words_each_size = {len(w):0 for w in all_words}

        for w in all_words:
            words_each_size[len(w)] += 1

        print(words_each_size)
        sized_words = [w for w in all_words if len(w) == size]

        return sized_words

    def time_a_star(self, start, end, words):
        print('start: %s end: %s ladder: %s' %(start, end, self.a_star_search(start, end, words)))

    def test_time_searches(self):
        words = self.get_words()
        start = words[random.randint(1,len(words))]
        end =  words[random.randint(1,len(words))]
        print(timeit(lambda:print(self.time_a_star(start, end, words)), number=1))


    def runTests(self):
        profile.runctx('self.test_time_searches()', globals(), locals())

    def test(self, start, end):
        self.start = start
        self.end = end
        words = self.get_words()
        print(self.a_star_search(start, end, words))
