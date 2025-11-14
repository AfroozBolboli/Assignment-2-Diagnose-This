from circuitplotter import plot_circuit
from guesscomponentsgame import choose_components, score_function
from conflictsets import ConflictSetRetriever
from hittingsets import run_hitting_set_algorithm
from os.path import join
import time
from heuristic import BFSHeuristic, SimpleHeuristic, FrequencyHeuristic, DFSHeuristic

def run_diagnosis_with_heuristicsMicha():
    """
    Runs a simple heuristic exploration showing the order of reasoning steps.
    """
    root = BFSHeuristic("Diagnose Circuit", 5)
    csets = BFSHeuristic("Find Conflict Sets", 3)
    hsets = BFSHeuristic("Compute Hitting Sets", 2)
    visualize = BFSHeuristic("Visualize Results", 7)

    root.add_child(csets)
    root.add_child(hsets)
    root.add_child(visualize)

    csets.add_child(BFSHeuristic("Analyze components", 4))
    csets.add_child(BFSHeuristic("Detect inconsistencies", 1))
    hsets.add_child(BFSHeuristic("Generate minimal sets", 3))
    hsets.add_child(BFSHeuristic("Evaluate diagnoses", 2))
    visualize.add_child(BFSHeuristic("Plot circuit", 6))
    visualize.add_child(BFSHeuristic("Print diagnosis summary", 8))

    print("\n=== Heuristic Reasoning Outcome BFSHeuristic ===")
    explore(root)
    print("===================================\n")



    simple_h = SimpleHeuristic(conflict_sets)
    bfs_h = BFSHeuristic(conflict_sets)


    # Choose which heuristic to use
    #heuristic = BFSHeuristic()  # or SimpleHeuristic()
    heuristic = SimpleHeuristic()  # or SimpleHeuristic()

    # Run hitting set algorithm with the heuristic
    hitting_sets, minimal_hitting_sets = run_hitting_set_algorithm(conflict_sets, heuristic)

    print("Hitting sets:", hitting_sets)
    print("Minimal hitting sets:", minimal_hitting_sets)

if __name__ == '__main__':
    document = "circuit2.txt"
    game = True

    # It only makes sense to play the game if you have the hitting set algorithm implemented.
    if game:
        # If you play the game, choose conflict sets, compute hitting sets:
        plot_circuit(document)
        chosen_conflict_sets = choose_components()
        print("Your chosen conflict sets:", chosen_conflict_sets)
        heuristic = SimpleHeuristic(chosen_conflict_sets)
        
        start = time.time()
        chosen_hitting_sets, chosen_minimal_hitting_sets = run_hitting_set_algorithm(chosen_conflict_sets, heuristic)
        end = time.time()
        print("Your hitting sets:", chosen_hitting_sets)
        print("Your minimal hitting sets:", chosen_minimal_hitting_sets, "\n")
        print("The running time: ",end-start)

    # Collect conflict sets:
    csr = ConflictSetRetriever(join("circuits", document))
    conflict_sets = csr.retrieve_conflict_sets()
    print("Actual conflict sets:", conflict_sets)
    
    # Collect minimal hitting sets:
    if len(conflict_sets) == 0:
        print("This circuit works correctly, there are no faulty components!")
    else:
        heuristic = SimpleHeuristic(conflict_sets)
        hitting_sets, minimal_hitting_sets = run_hitting_set_algorithm(conflict_sets, heuristic)
        print("Hitting sets:", hitting_sets)
        print("Minimal hitting sets:", minimal_hitting_sets, "\n")

    # Give score on similarity between the two sets:
    if game:
        score = score_function(conflict_sets, chosen_conflict_sets)
        print(f"Your score: {score:.2f}%")

    # Run heuristic reasoning exploration:
    #run_diagnosis_with_heuristicsMicha()
    #run_diagnosis_with_heuristics()

#[['X1', 'X2'], ['X3', 'X4'], ['X2', 'X4']]
# Your score: 33.33%
# The running time:  0.0001289844512939453 SIMPLE
# The running time:  0.00013589859008789062
# The running time:  0.00015115737915039062