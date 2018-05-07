# graph_traversal
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