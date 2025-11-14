from heuristic import BFSHeuristic, SimpleHeuristic

def run_hitting_set_algorithm(conflict_sets, heuristic):
    # Goal: The smallest possible explanation for the observed faults
    """
    Algorithm that handles the entire process from conflict sets to hitting sets

    :param conflict_sets: list of conflict sets as list
    :return: the hitting sets and minimal hitting sets as list of lists
    """

    # Check to see if the hitting set and conflicts have an intersection
    def is_intersected(hitting_set, conflict_sets):
        intersections = 0
        for conflict in conflict_sets:
            if set(hitting_set) & set(conflict):
                intersections += 1
        return intersections == len(conflict_sets)
     
    # Check to see if it is a minimal hitting set
    def is_minimal(hitting_set, minimal_sets):
        for minimal in minimal_sets:
            if set(minimal).issubset(set(hitting_set)):
                return False
        return True 
    
    # Variables 
    # Our representation for the tree structure
    to_explore_nodes = [[]] #tree nodes
    minimal_sets = []

    # While there are still codes to explore go on
    # Implementing hitting set tree algorithm
    explored_count = 0
    while len(to_explore_nodes) > 0 :
        explored_count += 1
        # Use of heuristics 
        best_score = None
        best_node = None
        for node in to_explore_nodes:
            score = heuristic.evaluate(node) 
            if best_score is None or score < best_score:
                best_score = score
                best_node = node


        ongoing_node = best_node
        to_explore_nodes.remove(ongoing_node)

        # Instead of pop we should implement the heuritics here
        print("Exploring:", ongoing_node)
        print("To explore next:", to_explore_nodes)
        # In case it is minimal
        if is_intersected(ongoing_node, conflict_sets):
            if is_minimal(ongoing_node, minimal_sets):
                minimal_sets.append(list(ongoing_node))
            continue
        
        # In case a conflict is not overlapped with the hitting set find the first conflict
        not_hit_yet = None
        for conflict in conflict_sets:
            if set(conflict).isdisjoint(set(ongoing_node)):
                not_hit_yet = conflict
                break
        
        if not_hit_yet is not None:
            # For every component in the conflict set add to to_explore_nodes
            for candidate in not_hit_yet:
                new_node = ongoing_node + [candidate]
                is_candidate = True

                # Check if candidate is already part of the to_explore_nodes list 
                for node in to_explore_nodes:
                    if set(new_node).issubset(set(node)):
                        is_candidate = False
                        break
                
                # Check to see if the candidate is already part of the minimal sets
                for minimal in minimal_sets:
                    if set(new_node).issubset(set(minimal)):
                        is_candidate = False
                        break 

                if is_candidate:
                    to_explore_nodes.append(new_node)
            # Make Hitting sets which are possible combination of different conflicts 
    hitting_sets = minimal_sets 
    print('explored nodes: ', explored_count)
    return hitting_sets,minimal_sets
