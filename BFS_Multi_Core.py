
from collections import defaultdict
from timeit import timeit
import random
import cProfile as profile
import multiprocessing as mp
from multiprocessing import Queue as Queue
from multiprocessing import Pool
import time
import os

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

class BFS_Multi_Core:
    class Node:

        def __init__(self, word, previous):
            self.word = word
            self.previous = previous

        def __lt__(self, other):
            return self.f < other.f

        def __str__(self):
            return '{}'.format(self.word)

    def __init__(self):
        print('initializing')
        #IF you want to change the words, change start and end here.  If you want to do a larger size word pass in an int with the size of the words you want to generate to get_words
        self.neighbors = defaultdict(list)
        self.q = Queue()
        self.queueSet = set()
        self.closedSet = set()
        self.words = self.get_words()
        self.start = self.words[random.randint(1,len(self.words))]
        self.end =  self.words[random.randint(1,len(self.words))]
        self.completed_graph = False
        self.path = []
        self.neighbors = self.generate_neighbors(self.words)

    def setup_self(self, q, qSet, closedSet, start, end ):
        self.q = q
        self.queueSet = qSet
        self.closedSet = closedSet
        self.start = start
        self.end = end

    def get_words(self, size=5):
        all_words = [w.strip().lower() for w in open('words.txt')]

        # print('total words: ' , len(all_words))
        words_each_size = {len(w):0 for w in all_words}

        for w in all_words:
            words_each_size[len(w)] += 1

        # print(words_each_size)
        sized_words = [w for w in all_words if len(w) == size]

        self.words = sized_words
        return sized_words


    def generate_neighbors(self,words):
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
        self.completed_graph = True
        path = [node.word]
        while node.previous != None:
            temp = node.previous
            node = node.previous
            path.append(temp.word)

        p = path[::-1]

        self.path = p
        return ' -> '.join(p)


    def search_for_path(self, q, queueSet, closedSet):
        # print('inside search_for_path pid: %s  ppid: %s' %(os.getpid(), os.getppid()))
        if(not self.completed_graph):
            subtree = q.get()


            for child in self.neighbors[subtree.word]:
                for c in child:
                    if c in closedSet:
                        continue


                    if c not in queueSet:

                        if c == self.end:
                            print('FINISHED!!!!!!!!!' * 5)
                            endNode = BFS_Multi_Core.Node(c,subtree)
                            return self.reconstruct_path(endNode)


                        q.put(BFS_Multi_Core.Node(c,subtree))
                        queueSet.add(c)


            closedSet.add(subtree.word)
            # print('word: ', subtree.word)
        return self.callback(q, closedSet, queueSet)

    def callback(self, a,b,c):
        self.q = a
        self.queueSet = c
        self.closedSet = b
        return (a,b,c)


    def breadth_first_search(self, s=None, e=None, w=None):
    #start: teems end: cress ladder: teems teens teeny teety teaty teasy trasy trass crass cress
        if s != None and e != None and w != None:
            start = s
            end = e
            words = w

        queueSet = set()
        closedSet = set()
        pool = mp.Pool()
        que = mp.Manager().Queue()

        self.setup_self(que,queueSet,closedSet,start,end)
        que.put(BFS_Multi_Core.Node(start,None))
        holder = (que,queueSet,closedSet)

        while not holder[0].empty() and holder[0] != None and not self.completed_graph:
            result = pool.apply_async(self.search_for_path,(holder[0],holder[1],holder[2]))
            holder = result.get(timeout=1)

            if len(holder) != 3:
                return holder


        msg = 'No way found! between %s - %s' %(start, end)
        return msg

    def time_breadth_first(self, start, end, words):
        print('start: %s end: %s ladder: %s' %(start, end, self.breadth_first_search(start, end, words)))

    def test_time_searches(self):
        print(timeit(lambda:print(self.time_breadth_first(self.words[random.randint(1,len(self.words))], self.words[random.randint(1,len(self.words))], self.words)), number=1))

    def runTests(self):
        profile.runctx('self.test_time_searches()', globals(), locals())


    def test(self, start, end):
        self.start = start
        self.end = end
        # self.words = words
        print(self.breadth_first_search(start, end, self.words))

if __name__ == '__main__':
    pass
