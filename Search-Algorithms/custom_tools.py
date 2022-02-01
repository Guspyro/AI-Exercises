# graph classes
class Node:
    x = 0
    y = 0
    connections = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connections = list()

    def connect_to(self, node):
        if isinstance(node, Node):
            self.connections.append(node)

    def get_pos(self):
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Edge:
    nodeA = None
    nodeB = None

    def __init__(self, nodeA, nodeB):
        if isinstance(nodeA, Node) and isinstance(nodeB, Node):
            self.nodeA = nodeA
            self.nodeB = nodeB


# geometry classes
class Geometry:

    @staticmethod
    def line_intersection(edge1, edge2):
        A = Edge(Node(edge1[0][0], edge1[0][1]), Node(edge1[1][0], edge1[1][1]))
        B = Edge(Node(edge2[0][0], edge2[0][1]), Node(edge2[1][0], edge2[1][1]))
        return Geometry.ccw(A.nodeA, B.nodeA, B.nodeB) != Geometry.ccw(A.nodeB, B.nodeA, B.nodeB) and Geometry.ccw(A.nodeA, A.nodeB, B.nodeA) != Geometry.ccw(A.nodeA ,A.nodeB, B.nodeB)

    @staticmethod
    def ccw(A, B, C):
        return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

    @staticmethod
    def get_polygon_edges(polygon):
        edges = list()
        for vertices_index in range(0, len(polygon)):
            if vertices_index == len(polygon) - 1:
                edges.append(Edge(Node(polygon[vertices_index][0], polygon[vertices_index][1]), Node(polygon[0][0], polygon[0][1])))
                return edges
            else:
                edges.append(Edge(Node(polygon[vertices_index][0], polygon[vertices_index][1]), Node(polygon[vertices_index + 1][0], polygon[vertices_index + 1][1])))
        return None
