import numpy as np
import random
import matplotlib.pyplot as plt
from collections import deque
import os


def generate_grid(n, obstacle_density):
    """
    Generates an n x n grid with obstacles placed based on the obstacle density.
    The number of obstacles is fixed based on the density.
    """
    total_cells = n * n
    total_obstacles = int(total_cells * obstacle_density)
    grid = np.zeros((n, n), dtype=int)
    
    # All positions excluding the start and end positions
    positions = [(i, j) for i in range(n) for j in range(n)]
    positions.remove((0, 0))
    positions.remove((n-1, n-1))
    
    # If total obstacles exceed available positions, adjust accordingly
    max_obstacles = len(positions)
    if total_obstacles > max_obstacles:
        total_obstacles = max_obstacles
    
    # Randomly select positions for obstacles
    obstacle_positions = random.sample(positions, total_obstacles)
    
    for pos in obstacle_positions:
        grid[pos] = -1  # -1 represents an obstacle
        
    return grid


def find_best_paths(grid):
    """
    Finds the number of best paths from (0, 0) to (n-1, n-1) with the least number of turns.
    Uses BFS to find all optimal paths.
    """
    n = grid.shape[0]
    if grid[0][0] == -1 or grid[n-1][n-1] == -1:
        return 0, float('inf')  # No path if start or end is blocked

    # Directions: right (0), down (1)
    directions = [
        (0, 1, 0),  # Right
        (1, 0, 1)   # Down
    ]

    # Visited array: stores minimum turns to reach a cell with a given direction
    visited = [[(float('inf'), -1) for _ in range(n)] for _ in range(n)]

    queue = deque()
    # Start from (0,0) with no direction and zero turns
    queue.append((0, 0, -1, 0))  # x, y, dir, turns
    visited[0][0] = (0, -1)

    min_turns = float('inf')
    best_path_count = 0

    while queue:
        x, y, dir_prev, turns = queue.popleft()

        if (x, y) == (n - 1, n - 1):
            if turns < min_turns:
                min_turns = turns
                best_path_count = 1
            elif turns == min_turns:
                best_path_count += 1
            continue

        for dx, dy, dir_new in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != -1:
                # Calculate new number of turns
                if dir_prev == -1:  # Starting cell
                    new_turns = 0
                elif dir_prev != dir_new:
                    new_turns = turns + 1
                else:
                    new_turns = turns

                # If we've found a path with fewer turns, update
                if new_turns < visited[nx][ny][0]:
                    visited[nx][ny] = (new_turns, dir_new)
                    queue.append((nx, ny, dir_new, new_turns))
                elif new_turns == visited[nx][ny][0] and dir_new != visited[nx][ny][1]:
                    # If same number of turns but different direction, still explore
                    visited[nx][ny] = (new_turns, dir_new)
                    queue.append((nx, ny, dir_new, new_turns))

    return best_path_count, min_turns


def find_all_best_paths_with_turns(grid, min_turns):
    """
    Finds all paths with the minimum number of turns from (0, 0) to (n-1, n-1).
    """
    n = grid.shape[0]
    if grid[0][0] == -1 or grid[n-1][n-1] == -1:
        return 0  # No path if start or end is blocked

    # Directions: right (0), down (1)
    directions = [
        (0, 1, 0),  # Right
        (1, 0, 1)   # Down
    ]

    queue = deque()
    # Start from (0,0) with no direction and zero turns
    queue.append((0, 0, -1, 0))  # x, y, dir, turns

    best_path_count = 0

    while queue:
        x, y, dir_prev, turns = queue.popleft()

        if (x, y) == (n - 1, n - 1) and turns == min_turns:
            best_path_count += 1
            continue

        for dx, dy, dir_new in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != -1:
                # Calculate new number of turns
                if dir_prev == -1:  # Starting cell
                    new_turns = 0
                elif dir_prev != dir_new:
                    new_turns = turns + 1
                else:
                    new_turns = turns

                # Only explore paths with minimum turns
                if new_turns <= min_turns:
                    queue.append((nx, ny, dir_new, new_turns))

    return best_path_count


def simulate_best_path_counts(n_values, obstacle_densities, simulations_per_point=5):
    """
    Simulates the best path counts for different n values and obstacle densities.
    Returns a dictionary with results for plotting.
    """
    results = {}
    for density in obstacle_densities:
        best_path_counts = []
        for n in n_values:
            total_best_paths = 0
            for _ in range(simulations_per_point):
                grid = generate_grid(n, density)
                _, min_turns = find_best_paths(grid)
                if min_turns < float('inf'):
                    num_best_paths = find_all_best_paths_with_turns(grid, min_turns)
                    total_best_paths += num_best_paths
            average = total_best_paths / simulations_per_point
            best_path_counts.append(average)
        results[density] = best_path_counts
    return results


def plot_best_path_counts(n_values, results, obstacle_densities):
    """
    Plots the results of the best path count simulation.
    """
    save_folder = 'result_images'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    plt.figure(figsize=(12, 8))
    for density, best_path_counts in results.items():
        plt.plot(n_values, best_path_counts, marker='o', label=f'Density: {density}')
    plt.title('Best Path Counts vs Grid Size for Different Obstacle Densities')
    plt.xlabel('Grid Size (n)')
    plt.ylabel('Average Number of Best Paths')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_folder, 'best_path_count.png'))
    plt.close()


def best_path_count_main():
    n_values = range(2, 17)  # Grid sizes from 2x2 to 16x16
    obstacle_densities = [0.0, 0.1, 0.2, 0.3, 0.4]  # Different obstacle densities
    simulations_per_point = 10000  # Number of simulations to average for each point
    random.seed(11505050)
    
    results = simulate_best_path_counts(n_values, obstacle_densities, simulations_per_point)
    plot_best_path_counts(n_values, results, obstacle_densities)
