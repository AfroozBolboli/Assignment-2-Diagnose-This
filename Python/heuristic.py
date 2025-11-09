import heapq

class HeuristicNode:
    """
    Node represented in a heuristic structure.
    For each node: a name + heuristic score + and child nodes.
    Lower heuristic = higher priority.
    """
    def __init__(self, name, heuristic_score):
        self.name = name
        self.heuristic_score = heuristic_score
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __lt__(self, other):
        # Compare nodes
        return self.heuristic_score < other.heuristic_score


def explore(start_node):
    # best-first search for exploring
    frontier = []
    heapq.heappush(frontier, start_node)

    print("Exploration order (lower heuristic = higher priority):\n")

    while frontier:
        current = heapq.heappop(frontier)
        print(f"→ {current.name} (h = {current.heuristic_score})")

        for child in current.children:
            heapq.heappush(frontier, child)


if __name__ == "__main__":
    # starting state
    root = HeuristicNode("Diagnose Circuit", heuristic_score=5)

    # Possible reasoning paths
    csets = HeuristicNode("Find Conflict Sets", heuristic_score=3)
    hsets = HeuristicNode("Compute Hitting Sets", heuristic_score=2)
    visualize = HeuristicNode("Visualize Results", heuristic_score=7)

    root.add_child(csets)
    root.add_child(hsets)
    root.add_child(visualize)

    # more reasoning layers
    csets.add_child(HeuristicNode("Analyze components", heuristic_score=4))
    csets.add_child(HeuristicNode("Detect inconsistencies", heuristic_score=1))

    hsets.add_child(HeuristicNode("Generate minimal sets", heuristic_score=3))
    hsets.add_child(HeuristicNode("Evaluate diagnoses", heuristic_score=2))

    visualize.add_child(HeuristicNode("Plot circuit", heuristic_score=6))
    visualize.add_child(HeuristicNode("Print diagnosis summary", heuristic_score=8))

    # Explore using heuristics
    explore(root)
