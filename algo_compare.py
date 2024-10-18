import random
import sys
import time
import math
import matplotlib.pyplot as plt
import os
from collections import deque
import heapq

sys.setrecursionlimit(1000000)  # Increase recursion limit if necessary

def generate_grid(n, obstacle_density):
    total_cells = n * n
    total_obstacles = int(total_cells * obstacle_density)
    grid = [[0 for _ in range(n)] for _ in range(n)]
    positions = [(i, j) for i in range(n) for j in range(n)]
    positions.remove((0, 0))
    positions.remove((n - 1, n - 1))
    max_obstacles = len(positions)
    if total_obstacles > max_obstacles:
        total_obstacles = max_obstacles
    obstacle_positions = random.sample(positions, total_obstacles)
    for pos in obstacle_positions:
        grid[pos[0]][pos[1]] = -1
    return grid

# Recursive Method
def recursive_paths(grid, x, y, dir_prev, turns, min_turns, memo):
    n = len(grid)
    if (x, y, dir_prev, turns) in memo:
        return memo[(x, y, dir_prev, turns)]
    if x == n - 1 and y == n - 1:
        if turns < min_turns[0]:
            min_turns[0] = turns
            return 1
        elif turns == min_turns[0]:
            return 1
        else:
            return 0
    if turns > min_turns[0]:
        return 0
    total_paths = 0
    directions = [("right", 0, 1), ("down", 1, 0)]
    for dir_new, dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != -1:
            if dir_prev is None:
                new_turns = turns
            elif dir_prev != dir_new:
                new_turns = turns + 1
            else:
                new_turns = turns
            total_paths += recursive_paths(grid, nx, ny, dir_new, new_turns, min_turns, memo)
    memo[(x, y, dir_prev, turns)] = total_paths
    return total_paths

def count_best_paths_recursive(grid):
    n = len(grid)
    if grid[0][0] == -1 or grid[n - 1][n - 1] == -1:
        return None, None
    min_turns = [float('inf')]
    memo = {}
    try:
        total_paths = recursive_paths(grid, 0, 0, None, 0, min_turns, memo)
        if min_turns[0] == float('inf'):
            return None, None  # No path found
        return total_paths, min_turns[0]
    except RecursionError:
        return None, None  # Recursion limit exceeded

# Dynamic Programming Method
def count_best_paths_dp(grid):
    n = len(grid)
    if grid[0][0] == -1 or grid[n - 1][n - 1] == -1:
        return 0, None
    dp = [[[float('inf')] * 2 for _ in range(n)] for _ in range(n)]
    paths = [[[0] * 2 for _ in range(n)] for _ in range(n)]
    queue = deque()
    # Start from (0, 0), with initial directions
    for dir_new_idx, (dir_new, dx, dy) in enumerate([("right", 0, 1), ("down", 1, 0)]):
        nx, ny = dx, dy
        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != -1:
            dp[nx][ny][dir_new_idx] = 0
            paths[nx][ny][dir_new_idx] = 1
            queue.append((nx, ny, dir_new_idx, 0))
    min_turns = float('inf')
    while queue:
        x, y, dir_prev, turns = queue.popleft()
        if x == n - 1 and y == n - 1:
            if turns < min_turns:
                min_turns = turns
        directions = [("right", 0, 1), ("down", 1, 0)]
        for dir_new_idx, (dir_new, dx, dy) in enumerate(directions):
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != -1:
                if dir_prev != dir_new_idx:
                    new_turns = turns + 1
                else:
                    new_turns = turns
                if new_turns > min_turns:
                    continue
                if dp[nx][ny][dir_new_idx] > new_turns:
                    dp[nx][ny][dir_new_idx] = new_turns
                    paths[nx][ny][dir_new_idx] = paths[x][y][dir_prev]
                    queue.append((nx, ny, dir_new_idx, new_turns))
                elif dp[nx][ny][dir_new_idx] == new_turns:
                    paths[nx][ny][dir_new_idx] += paths[x][y][dir_prev]
    total_paths = 0
    if min_turns < float('inf'):
        for dir_idx in range(2):
            if dp[n - 1][n - 1][dir_idx] == min_turns:
                total_paths += paths[n - 1][n - 1][dir_idx]
    else:
        return 0, None
    return total_paths, min_turns

# Combinatorial Method (without obstacles)
def count_best_paths_combinatorial(n):
    # Number of paths with minimal number of turns (1 turn)
    if n < 2:
        return 1, 0  # Only one cell
    return 2, 1  # Two paths: all right then down, or all down then right

# Dijkstra's Algorithm Method (minimizing number of turns)
def count_best_paths_dijkstra(grid):
    n = len(grid)
    if grid[0][0] == -1 or grid[n - 1][n - 1] == -1:
        return 0, None
    # Directions: 0 - right, 1 - down
    directions = [("right", 0, 1), ("down", 1, 0)]
    heap = []
    # Initialize heap with possible starting directions
    for dir_idx, (dir_name, dx, dy) in enumerate(directions):
        nx, ny = dx, dy
        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != -1:
            heapq.heappush(heap, (0, nx, ny, dir_idx))
    # Initialize DP tables
    min_turns = [[ [float('inf')] * 2 for _ in range(n)] for _ in range(n)]
    path_counts = [[ [0] * 2 for _ in range(n)] for _ in range(n)]
    # Set initial states
    for dir_idx, (dir_name, dx, dy) in enumerate(directions):
        nx, ny = dx, dy
        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != -1:
            min_turns[nx][ny][dir_idx] = 0
            path_counts[nx][ny][dir_idx] = 1
    while heap:
        turns, x, y, dir_prev = heapq.heappop(heap)
        # If we reached the end, continue to find all minimal paths
        if x == n - 1 and y == n - 1:
            continue
        for new_dir_idx, (dir_new, dx, dy) in enumerate(directions):
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != -1:
                if new_dir_idx != dir_prev:
                    new_turns = turns + 1
                else:
                    new_turns = turns
                if new_turns < min_turns[nx][ny][new_dir_idx]:
                    min_turns[nx][ny][new_dir_idx] = new_turns
                    path_counts[nx][ny][new_dir_idx] = path_counts[x][y][dir_prev]
                    heapq.heappush(heap, (new_turns, nx, ny, new_dir_idx))
                elif new_turns == min_turns[nx][ny][new_dir_idx]:
                    path_counts[nx][ny][new_dir_idx] += path_counts[x][y][dir_prev]
    # Find minimal turns at destination
    final_min_turns = float('inf')
    total_paths = 0
    for dir_idx in range(2):
        if min_turns[n - 1][n - 1][dir_idx] < final_min_turns:
            final_min_turns = min_turns[n - 1][n - 1][dir_idx]
            total_paths = path_counts[n - 1][n - 1][dir_idx]
        elif min_turns[n - 1][n - 1][dir_idx] == final_min_turns:
            total_paths += path_counts[n - 1][n - 1][dir_idx]
    if final_min_turns == float('inf'):
        return 0, None
    return total_paths, final_min_turns

def algo_compare_main():
    import time
    random.seed(11505050)
    save_folder = 'result_images'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    grid_sizes = [10, 50, 100, 200, 300, 400, 500, 600]  # Adjusted for demonstration
    obstacle_densities = [0.0, 0.1, 0.3, 0.5]
    methods = ['Recursive', 'Dynamic Prog.', 'Combinatorial', 'Dijkstra']

    # Data structures to store results
    results = {method: {density: {'sizes': [], 'times': []} for density in obstacle_densities} for method in methods}

    print(f"{'Grid Size':<10} {'Density':<10} {'Method':<15} {'Time (s)':<10}")
    print("-" * 50)

    for n in grid_sizes:
        for density in obstacle_densities:
            grid = generate_grid(n, density)

            # Recursive Method
            if n <= 1000:  # Limit recursive method to smaller grids to prevent excessive computation
                start_time = time.time()
                _, _ = count_best_paths_recursive(grid)
                time_rec = time.time() - start_time
                results['Recursive'][density]['sizes'].append(n)
                results['Recursive'][density]['times'].append(time_rec)
                print(f"{n:<10} {density:<10} {'Recursive':<15} {time_rec:<10.4f}")
            else:
                print(f"{n:<10} {density:<10} {'Recursive':<15} {'N/A':<10}")

            # Dynamic Programming Method
            start_time = time.time()
            _, _ = count_best_paths_dp(grid)
            time_dp = time.time() - start_time
            results['Dynamic Prog.'][density]['sizes'].append(n)
            results['Dynamic Prog.'][density]['times'].append(time_dp)
            print(f"{n:<10} {density:<10} {'Dynamic Prog.':<15} {time_dp:<10.4f}")

            # Combinatorial Method (only applicable without obstacles)
            if density == 0.0:
                start_time = time.time()
                _, _ = count_best_paths_combinatorial(n)
                time_comb = time.time() - start_time
                results['Combinatorial'][density]['sizes'].append(n)
                results['Combinatorial'][density]['times'].append(time_comb)
                print(f"{n:<10} {density:<10} {'Combinatorial':<15} {time_comb:<10.4f}")
            else:
                print(f"{n:<10} {density:<10} {'Combinatorial':<15} {'N/A':<10}")

            # Dijkstra's Method
            start_time = time.time()
            _, _ = count_best_paths_dijkstra(grid)
            time_dijkstra = time.time() - start_time
            results['Dijkstra'][density]['sizes'].append(n)
            results['Dijkstra'][density]['times'].append(time_dijkstra)
            print(f"{n:<10} {density:<10} {'Dijkstra':<15} {time_dijkstra:<10.4f}")

    # Plotting execution times for all methods and densities in the same image
    plt.figure(figsize=(14, 8))
    markers = {'Recursive': 'o', 'Dynamic Prog.': 's', 'Combinatorial': '^', 'Dijkstra': 'D'}
    linestyles = ['-', '--', '-.', ':']
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan']
    for method_idx, method in enumerate(methods):
        for density_idx, density in enumerate(obstacle_densities):
            sizes = results[method][density]['sizes']
            times = results[method][density]['times']
            if sizes:
                label = f"{method}, density={density}"
                linestyle = linestyles[density_idx % len(linestyles)]
                color = colors[method_idx % len(colors)]
                plt.plot(sizes, times, marker=markers.get(method, 'o'), linestyle=linestyle, color=color, label=label)
    plt.title('Execution Time vs Grid Size for All Methods and Densities', fontsize=16)
    plt.xlabel('Grid Size (n)', fontsize=14)
    plt.ylabel('Execution Time (s)', fontsize=14)
    plt.legend(fontsize=12, loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.tight_layout()
    # Save the figure
    filename = 'execution_time_all_methods_and_densities.png'
    plt.savefig(os.path.join(save_folder, filename), dpi=300)
    plt.close()

