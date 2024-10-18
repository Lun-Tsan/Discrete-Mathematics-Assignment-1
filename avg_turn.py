import numpy as np
import matplotlib.pyplot as plt
import random
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
    
    # Remove the start and end positions from possible obstacle positions
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

def find_best_path_with_least_turns(grid):
    """
    Finds the best path from (0,0) to (n-1,n-1) with the least number of turns.
    Returns the number of turns if a path is found, or None if no path exists.
    """
    n = grid.shape[0]
    if grid[0][0] == -1 or grid[n-1][n-1] == -1:
        return None  # No path if start or end is blocked

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

    min_turns = None

    while queue:
        x, y, dir_prev, turns = queue.popleft()

        if (x, y) == (n - 1, n - 1):
            if min_turns is None or turns < min_turns:
                min_turns = turns
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

    return min_turns

def simulate(n_values, obstacle_densities, simulations_per_point=5):
    """
    Simulates the best path calculations for different n values and obstacle densities.
    Returns a dictionary with results for plotting.
    """
    results = {}
    for density in obstacle_densities:
        avg_turns = []
        for n in n_values:
            total_turns = 0
            successful_simulations = 0
            for _ in range(simulations_per_point):
                grid = generate_grid(n, density)
                min_turns = find_best_path_with_least_turns(grid)
                if min_turns is not None:
                    total_turns += min_turns
                    successful_simulations += 1
                else:
                    pass  # Do not include this simulation in the average
            if successful_simulations > 0:
                average_turns = total_turns / successful_simulations
            else:
                average_turns = 0  # Set to 0 when no paths were found
            avg_turns.append(average_turns)
        results[density] = avg_turns
    return results

def plot_results(n_values, results, obstacle_densities):
    """
    Plots the results of the simulation, handling cases where no paths were found.
    """
    save_folder = 'result_images'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    plt.figure(figsize=(12, 8))
    for density, avg_turns in results.items():
        x_values = n_values
        y_values = avg_turns
        plt.plot(x_values, y_values, marker='o', label=f'Density: {density}')
    
    # Mark points where average_turns == 0 (No Path Found)
    for density, avg_turns in results.items():
        no_path_indices = [i for i, avg_turn in enumerate(avg_turns) if avg_turn == 0]
        if no_path_indices:
            no_path_n_values = [n_values[i] for i in no_path_indices]
            no_path_y_values = [0 for _ in no_path_indices]
            plt.scatter(no_path_n_values, no_path_y_values, color='red', marker='x', s=100, label='No Path Found' if density == obstacle_densities[0] else "")
    
    plt.title('Average Number of Turns in Best Path vs Grid Size for Different Obstacle Densities')
    plt.xlabel('Grid Size (n)')
    plt.ylabel('Average Number of Turns in Best Path')
    plt.legend()
    plt.grid(True)
    # Save the figure
    plt.savefig(os.path.join(save_folder, 'average_turns.png'))
    plt.close()

def avg_turn_main():
    n_values = range(2, 17)  # Grid sizes from 2x2 to 16x16
    obstacle_densities = [0.0, 0.2, 0.4, 0.5, 0.7]  # Different obstacle densities
    simulations_per_point = 10000  # Number of simulations to average for each point
    random.seed(11505050)
    results = simulate(n_values, obstacle_densities, simulations_per_point)
    plot_results(n_values, results, obstacle_densities)

    # Optionally, print the results
    print("Grid Size (n) | Obstacle Density | Average Number of Turns")
    print("---------------------------------------------------------")
    for density in obstacle_densities:
        for idx, n in enumerate(n_values):
            avg_turns = results[density][idx]
            if avg_turns != 0:
                print(f"{n:<13} | {density:<16} | {avg_turns:<22.2f}")
            else:
                print(f"{n:<13} | {density:<16} | {'No Path Found':<22}")