class Node:
    def __init__(self, subject, relation, obj):
        self.subject = subject
        self.relation = relation
        self.obj = obj

class Graph:
    nodes: list[Node] = []