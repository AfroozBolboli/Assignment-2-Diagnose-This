import heapq

"""class BFSHeuristic:
    """ """
    Node represented in a heuristic structure.
    For each node: a name + heuristic score + and child nodes.
    Lower heuristic = higher priority.
    """ """
    def __init__(self, name, heuristic_score):
        self.name = name
        self.heuristic_score = heuristic_score
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __lt__(self, other):
        # compare nodes
        return self.heuristic_score < other.heuristic_score
    
    def score(self, hitting_set):
        """ """
        Basic BFS-style scoring:
        - smaller sets (shallower nodes) get higher score
        - doesn't focus on conflicts, only structure
        """ """
        depth_penalty = len(hitting_set)
        return -depth_penalty  # smaller depth = better (higher score)

    def evaluate(self, hitting_set):
        """  """
        Return value for sorting — lower = higher priority.
        """ """
        return -self.score(hitting_set)
""" 



# heuristic.py
import heapq

class BFSHeuristic:
    """
    BFS-style heuristic for hitting set search.
    Lower score = higher priority.
    """
    def __init__(self, conflict_sets):
        self.conflict_sets = conflict_sets

    def evaluate(self, node):
        """
        Give a heuristic score for a hitting set candidate.
        We'll reward hitting more conflicts and penalize larger sets.
        """
        conflicts_hit = sum(1 for conflict in self.conflict_sets if set(node) & set(conflict))
        size_penalty = len(node)
        # Higher score = worse, so we negate it
        return -(conflicts_hit * 10 - size_penalty)


class SimpleHeuristic:
    #Rewards hitting sets that cover more conflicts and penalizes larger sets.
    
    def __init__(self, conflict_sets, w_conflict=10, w_size=1):
        """
        Args:
            conflict_sets (list of lists): the set of conflicts in the system
            w_conflict (int): weight for hitting a conflict
            w_size (int): penalty weight for hitting set size
        """
        self.conflict_sets = conflict_sets
        self.w_conflict = w_conflict
        self.w_size = w_size

    def score(self, hitting_set):
        """
        Compute the heuristic score for a hitting set.
        Higher score = better hitting set

        Args:
            hitting_set (list): a candidate hitting set

        Returns:
            int: heuristic score
        """
        # Count how many conflicts are hit
        conflicts_hit = sum(1 for conflict in self.conflict_sets 
                            if set(hitting_set) & set(conflict))

        # Penalize larger hitting sets
        size_penalty = len(hitting_set)

        # Compute total heuristic
        return self.w_conflict * conflicts_hit - self.w_size * size_penalty
    
    def evaluate(self, hitting_set):
        return -self.score(hitting_set)


class FrequencyHeuristic:
    def __init__(self, conflict_sets, w_freq=10, w_size=1):
        self.conflict_sets = conflict_sets
        self.w_freq = w_freq
        self.w_size = w_size

        # Count how often each element appears across all conflicts
        self.frequency = {}
        for conflict in conflict_sets:
            for comp in conflict:
                self.frequency[comp] = self.frequency.get(comp, 0) + 1

    def score(self, hitting_set):
        freq_score = sum(self.frequency.get(comp, 0) for comp in hitting_set)
        size_penalty = len(hitting_set)
        return self.w_freq * freq_score - self.w_size * size_penalty

    def evaluate(self, hitting_set):
        return -self.score(hitting_set)

class DFSHeuristic:
    """
    Depth-First Search–like heuristic.
    Prefers exploring deeper (larger) hitting sets first.
    Smaller sets get lower priority.
    """

    def __init__(self, conflict_sets, w_depth=5, w_size=1):
        """
        Args:
            conflict_sets (list of lists): known conflict sets
            w_depth (int): weight for depth preference
            w_size (int): penalty for set size
        """
        self.conflict_sets = conflict_sets
        self.w_depth = w_depth
        self.w_size = w_size

    def score(self, hitting_set):
        """
        Higher score = explore deeper (DFS-like)
        """
        # prefer larger sets (deeper)
        depth_score = self.w_depth * len(hitting_set)

        # reward conflicts hit (to avoid going random deep)
        conflicts_hit = sum(1 for conflict in self.conflict_sets 
                            if set(hitting_set) & set(conflict))

        # compute final score
        return depth_score + conflicts_hit - self.w_size * len(hitting_set)

    def evaluate(self, hitting_set):
        # Lower = higher priority (since heapq uses min-heap)
        return -self.score(hitting_set)
