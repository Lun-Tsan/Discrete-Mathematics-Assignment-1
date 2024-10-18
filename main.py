from possible_path import possible_path_main
from best_path_trend import best_path_trend_main
from avg_turn import avg_turn_main
from algo_compare import algo_compare_main

def main():
    # Run the possible_path module
    print("Running possible_path module...")
    possible_path_main()
    print("Finished possible_path module.\n")

    # Run the best_path_trend module
    print("Running best_path_trend module...")
    best_path_trend_main()
    print("Finished best_path_trend module.\n")

    # Run the avg_turn module
    print("Running avg_turn module...")
    avg_turn_main()
    print("Finished avg_turn module.\n")

    # Run the algo_compare module
    print("Running algo_compare module...")
    algo_compare_main()
    print("Finished algo_compare module.\n")

if __name__ == "__main__":
    main()
