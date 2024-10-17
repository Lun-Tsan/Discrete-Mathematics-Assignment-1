import matplotlib.pyplot as plt
import math

def factorial(n):
    return math.factorial(n)

def compute_total_paths(n):
    return factorial(2 * n - 2) // (factorial(n - 1) ** 2)

def compute_paths_with_t_turns(n, t):
    """
    Computes the number of paths from (0,0) to (n-1,n-1) with exactly t turns.
    """
    if t < 1 or t > 2 * n - 2:
        return 0
    paths = 0
    
    if t == 1:
        return 2
    else:
        k = t + 1
        m = n - 1
        # Ensure k - 1 is not greater than m - 1 to prevent negative factorial arguments
        if k - 1 > m - 1:  
            return 0  # Return 0 if k - 1 > m - 1, as combinations are not defined in this case
        compositions = combinations(m - 1, k - 1)
        paths = 2 * compositions ** 2
        return paths

def combinations(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def main():
    n_values = range(2, 17)  # Grid sizes from 2x2 to 10x10
    min_turns = 1  # Minimum number of turns
    min_plus_one_turns = 2  # Minimum number of turns plus one

    paths_with_min_turns = []
    paths_with_min_plus_one_turns = []

    for n in n_values:
        # Paths with minimal number of turns
        paths_min_turns = compute_paths_with_t_turns(n, min_turns)
        paths_with_min_turns.append(paths_min_turns)

        # Paths with minimal number of turns plus one
        paths_min_plus_one_turns = compute_paths_with_t_turns(n, min_plus_one_turns)
        paths_with_min_plus_one_turns.append(paths_min_plus_one_turns)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, paths_with_min_turns, marker='o', label='Paths with Min Turns (1 Turn)')
    plt.plot(n_values, paths_with_min_plus_one_turns, marker='s', label='Paths with Min Turns + 1 (2 Turns)')
    plt.title('Number of Best Paths vs Grid Size (n)')
    plt.xlabel('Grid Size (n)')
    plt.ylabel('Number of Best Paths')
    plt.xticks(n_values)
    plt.legend()
    plt.grid(True)
    plt.show()

    # Print the results
    print("Grid Size (n) | Paths with Min Turns | Paths with Min Turns + 1")
    print("-------------------------------------------------------------")
    for idx, n in enumerate(n_values):
        print(f"{n:13} | {paths_with_min_turns[idx]:20} | {paths_with_min_plus_one_turns[idx]:24}")

if __name__ == "__main__":
    main()
