class SimpleHeuristic:
    # Rewards hitting sets with more conflicts and punishes larger sets.
    # Simpleheuristic is insspired by BFS which was also used in the previous assignment

    def __init__(self, conflict_sets, w_conflict=10, w_size=1):
        self.conflict_sets = conflict_sets
        self.w_conflict = w_conflict  # weight for hitting a conflict
        self.w_size = w_size          # penalty for hitting set size

    def score(self, hitting_set):
        # Count how many conflicts are hit
        conflicts = 0
        for conflict in self.conflict_sets:
            if set(hitting_set) & set(conflict):
                conflicts += 1

        # Punishes larger hitting sets
        size_cost = len(hitting_set)

        # Compute total heuristic
        total_score = self.w_conflict * conflicts - self.w_size * size_cost
        return total_score

    def evaluate(self, hitting_set):
        # Lower = higher priority
        return -self.score(hitting_set)

class FrequencyHeuristic:
    # FrequencyHeuristic prefers components that appear in many conflicts
    # It penalizes hitting sets that are too large

    def __init__(self, conflict_sets, w_freq=10, w_size=1):
        self.conflict_sets = conflict_sets
        self.w_freq = w_freq   # weight for frequency
        self.w_size = w_size   # penalty for size
        self.frequency = {}

        #  How many times each component appears in conflict sets
        for conflict in conflict_sets:
            for component in conflict:
                if component in self.frequency:
                    self.frequency[component] += 1
                else:
                    self.frequency[component] = 1

    def score(self, hitting_set):
        # If component is a key -> returns value 
        # If not return 0 
        # Then sum all of them

        score = 0
        for component in hitting_set:
            score += self.frequency.get(component, 0)

        # To punish large hitting sets
        size_cost = len(hitting_set)

        # Final score
        return score * self.w_freq - self.w_size * size_cost

    def evaluate(self, hitting_set):
        # Lower value = higher priority for the algorithm
        return -self.score(hitting_set)


class DFSHeuristic:
    # DFSHeuristic prefers exploring larger hitting sets first. 
    # Smaller hitting sets have lower priority

    def __init__(self, conflict_sets, w_depth=4, w_size=1):

        self.conflict_sets = conflict_sets
        self.w_depth = w_depth # Weight
        self.w_size = w_size # Penalty for size 

    def score(self, hitting_set):
        # Deeper = Higher score
        depth_score = self.w_depth * len(hitting_set)

        # Conflicts hit: reward sets that cover more conflicts
        conflicts = 0
        for conflict in self.conflict_sets:
            if set(hitting_set) & set(conflict):
                conflicts += 1

        # Final score: larger sets + conflicts hit - penalty for size
        final_score = depth_score + conflicts - self.w_size * len(hitting_set)
        return final_score

    
    def evaluate(self, hitting_set):
        # Lower score = higher priority 
        return -self.score(hitting_set)
