import heapq

class HeuristicTreeNode:
    """
    Node represented in a HEURISTIC tree
    For each node: a name + heuristic score + and child nodes.
    Lower heuristic = higher priority 
    Class Holds the root node
    """
    def __init__(self, name, heuristic_score):
        self.name = name
        self.heuristic_score = heuristic_score
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __lt__(self, other):
        #Compare nodes
        return self.heuristic_score < other.heuristic_score


class HeuristicTree:
    """
    Build and explore the tree with heuristics
    Nodes with lower heuristic scores are made into branches first (NOTE: Afrooz please tell me if this is correct)
    (best first search with heapq)
    """
    def __init__(self, root):
        self.root = root

    def explore(self):
        #best-first search for exploring
        frontier = []
        heapq.heappush(frontier, self.root)

        print("Exploration order (lower heuristic = higher priority):\n")

        while frontier:
            current = heapq.heappop(frontier)
            print(f"→ {current.name} (h = {current.heuristic_score})")

            for child in current.children:
                heapq.heappush(frontier, child)


if __name__ == "__main__":
    # starting state
    root = HeuristicTreeNode("Diagnose Circuit", heuristic_score=5)

    # Possible reasoning paths
    csets = HeuristicTreeNode("Find Conflict Sets", heuristic_score=3)
    hsets = HeuristicTreeNode("Compute Hitting Sets", heuristic_score=2)
    visualize = HeuristicTreeNode("Visualize Results", heuristic_score=7)

    root.add_child(csets)
    root.add_child(hsets)
    root.add_child(visualize)

    # more reasoning layers (deeper?)
    csets.add_child(HeuristicTreeNode("Analyze components", heuristic_score=4))
    csets.add_child(HeuristicTreeNode("Detect inconsistencies", heuristic_score=1))

    hsets.add_child(HeuristicTreeNode("Generate minimal sets", heuristic_score=3))
    hsets.add_child(HeuristicTreeNode("Evaluate diagnoses", heuristic_score=2))

    visualize.add_child(HeuristicTreeNode("Plot circuit", heuristic_score=6))
    visualize.add_child(HeuristicTreeNode("Print diagnosis summary", heuristic_score=8))

    # Create HEURISTIC tree
    tree = HeuristicTree(root)
    tree.explore()
