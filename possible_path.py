import numpy as np
import matplotlib.pyplot as plt
import random
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

def calculate_number_of_paths(grid):
    """
    Calculates the number of possible paths from the top-left corner to the
    bottom-right corner in a grid, considering obstacles.
    """
    n = grid.shape[0]
    dp = np.zeros((n, n), dtype=int)
    
    # If the starting cell is not an obstacle, set dp[0][0] to 1
    if grid[0][0] == -1:
        return 0
    else:
        dp[0][0] = 1

    # Initialize the first row and first column
    for i in range(1, n):
        if grid[i][0] == -1:
            dp[i][0] = 0
        else:
            dp[i][0] = dp[i-1][0]
    for j in range(1, n):
        if grid[0][j] == -1:
            dp[0][j] = 0
        else:
            dp[0][j] = dp[0][j-1]

    # Fill in the rest of the dp table
    for i in range(1, n):
        for j in range(1, n):
            if grid[i][j] == -1:
                dp[i][j] = 0
            else:
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
                
    return dp[n-1][n-1]

def simulate(n_values, obstacle_densities, simulations_per_point=5):
    """
    Simulates the path calculations for different n values and obstacle densities.
    Returns a dictionary with results for plotting.
    """
    results = {}
    for density in obstacle_densities:
        avg_paths = []
        for n in n_values:
            total_paths = 0
            for _ in range(simulations_per_point):
                grid = generate_grid(n, density)
                num_paths = calculate_number_of_paths(grid)
                total_paths += num_paths
            average = total_paths / simulations_per_point
            avg_paths.append(average)
        results[density] = avg_paths
    return results

def plot_results(n_values, results, obstacle_densities):
    """
    Plots the results of the simulation.
    """
    save_folder = 'result_images'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    plt.figure(figsize=(16, 8))
    zero_paths_label_added = False  # Flag to track if 'Zero Paths' label has been added
    for density, avg_paths in results.items():
        # Identify indices where avg_paths are below 1e-3
        zero_indices = [i for i, path in enumerate(avg_paths) if path < 1e-3]
        non_zero_indices = [i for i, path in enumerate(avg_paths) if path >= 1e-3]
        
        # Prepare data for plotting
        avg_paths_adjusted = []
        for path in avg_paths:
            if path < 1e-3:
                avg_paths_adjusted.append(1e-3)
            else:
                avg_paths_adjusted.append(path)
        
        # Plot the adjusted average paths
        plt.plot(n_values, avg_paths_adjusted, marker='o', label=f'Density: {density}')
        
        # Mark the zero paths
        if zero_indices:
            zero_n_values = [n_values[i] for i in zero_indices]
            zero_paths = [1e-3 for _ in zero_indices]
            if not zero_paths_label_added:
                plt.scatter(zero_n_values, zero_paths, color='red', marker='x', s=100, label='Zero Paths')
                zero_paths_label_added = True
            else:
                plt.scatter(zero_n_values, zero_paths, color='red', marker='x', s=100)
    
    plt.title('Possible Path Counts vs Grid Size for Different Obstacle Densities')
    plt.xlabel('Grid Size (n)')
    plt.ylabel('Average Number of Possible Paths (log scale)')
    plt.yscale('log')  # Use logarithmic scale for y-axis
    plt.legend()
    plt.grid(True)
    # Save the figure
    plt.savefig(os.path.join(save_folder, 'possible_paths.png'))
    plt.close()

def possible_path_main():
    n_values = range(2, 17)  # Grid sizes from 2x2 to 16x16
    obstacle_densities = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]  # Different obstacle densities
    simulations_per_point = 10000  # Number of simulations to average for each point
    random.seed(11505050)
    results = simulate(n_values, obstacle_densities, simulations_per_point)
    plot_results(n_values, results, obstacle_densities)