from AStar import AStar
from BFS import BFS
from BFS_Multi_Core import BFS_Multi_Core


def print_break():
    print('=' * 90)

def test_astar(tests):
    astar = AStar()

    for t in tests:
        astar.test(t[0], t[1])

    astar.runTests()
    print_break()

def test_bfs(tests):
    bfs = BFS()

    for t in tests:
        bfs.test(t[0], t[1])

    bfs.runTests()
    print_break()

def test_multicore(tests):
    bfs = BFS_Multi_Core()

    for t in tests:
        bfs.test(t[0], t[1])

    bfs.runTests()
    print_break()

def run_tests():
    a = ('break', 'brake')
    b = ('house', 'mouse')
    c = ('teems', 'cress')
    d = ('penna', 'bunny')
    e = ('bosom', 'dinky')
    f = ('epopt','fluty') # failure state, no path from epopt to fluty
    h = ('heinz', 'bahoe') # failure state
    tests = [a,h,b,c,d,e,f]
    test_astar(tests)
    test_bfs(tests)
    test_multicore(tests)

if __name__ == '__main__':
    run_tests()



