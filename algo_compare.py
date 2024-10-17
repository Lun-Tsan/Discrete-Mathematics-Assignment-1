import random
import sys
import time
import math
import matplotlib.pyplot as plt
from collections import deque

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
    max_turns = 2 * (n - 1)  # Maximum possible turns
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
    return 2, 1  # (number of paths, minimal turns)

def main():
    import time
    random.seed(11505050)
    grid_sizes = [5, 10, 20, 50, 100, 200, 500]
    obstacle_densities = [0.0, 0.1, 0.2]
    methods = ['Recursive', 'Dynamic Prog.', 'Combinatorial']

    # Data structures to store results
    results = {method: {density: {'sizes': [], 'times': [], 'paths': [], 'turns': []} for density in obstacle_densities} for method in methods}

    print(f"{'Grid Size':<10} {'Density':<10} {'Method':<15} {'Paths':<10} {'Turns':<10} {'Time (s)':<10}")
    print("-" * 65)

    for n in grid_sizes:
        for density in obstacle_densities:
            grid = generate_grid(n, density)

            # Recursive Method

            start_time = time.time()
            total_paths_rec, min_turns_rec = count_best_paths_recursive(grid)
            time_rec = time.time() - start_time
            results['Recursive'][density]['sizes'].append(n)
            results['Recursive'][density]['times'].append(time_rec)
            results['Recursive'][density]['paths'].append(total_paths_rec)
            results['Recursive'][density]['turns'].append(min_turns_rec)
            print(f"{n:<10} {density:<10} {'Recursive':<15} "
                    f"{total_paths_rec if total_paths_rec is not None else 'N/A':<10} "
                    f"{min_turns_rec if min_turns_rec is not None else 'N/A':<10} "
                    f"{time_rec:<10.4f}")

            # Dynamic Programming Method
            start_time = time.time()
            total_paths_dp, min_turns_dp = count_best_paths_dp(grid)
            time_dp = time.time() - start_time
            results['Dynamic Prog.'][density]['sizes'].append(n)
            results['Dynamic Prog.'][density]['times'].append(time_dp)
            results['Dynamic Prog.'][density]['paths'].append(total_paths_dp)
            results['Dynamic Prog.'][density]['turns'].append(min_turns_dp)
            print(f"{n:<10} {density:<10} {'Dynamic Prog.':<15} "
                  f"{total_paths_dp if total_paths_dp is not None else 'N/A':<10} "
                  f"{min_turns_dp if min_turns_dp is not None else 'N/A':<10} "
                  f"{time_dp:<10.4f}")

            # Combinatorial Method (only applicable without obstacles)
            if density == 0.0:
                start_time = time.time()
                total_paths_comb, min_turns_comb = count_best_paths_combinatorial(n)
                time_comb = time.time() - start_time
                results['Combinatorial'][density]['sizes'].append(n)
                results['Combinatorial'][density]['times'].append(time_comb)
                results['Combinatorial'][density]['paths'].append(total_paths_comb)
                results['Combinatorial'][density]['turns'].append(min_turns_comb)
                print(f"{n:<10} {density:<10} {'Combinatorial':<15} "
                      f"{total_paths_comb:<10} {min_turns_comb:<10} {time_comb:<10.4f}")
            else:
                print(f"{n:<10} {density:<10} {'Combinatorial':<15} {'N/A':<10} {'N/A':<10} {'N/A':<10}")

    # Plotting the execution times
    for method in methods:
        plt.figure(figsize=(12, 6))
        for density in obstacle_densities:
            sizes = results[method][density]['sizes']
            times = results[method][density]['times']
            plt.plot(sizes, times, marker='o', label=f'Density: {density}')
        plt.title(f'Execution Time vs Grid Size - {method}')
        plt.xlabel('Grid Size (n)')
        plt.ylabel('Execution Time (s)')
        plt.legend()
        plt.grid(True)
        plt.show()

    # Plotting the number of paths
    for method in methods:
        plt.figure(figsize=(12, 6))
        for density in obstacle_densities:
            sizes = results[method][density]['sizes']
            paths = results[method][density]['paths']
            plt.plot(sizes, paths, marker='o', label=f'Density: {density}')
        plt.title(f'Number of Best Paths vs Grid Size - {method}')
        plt.xlabel('Grid Size (n)')
        plt.ylabel('Number of Best Paths')
        plt.legend()
        plt.grid(True)
        plt.show()

    # Plotting the minimal number of turns (if applicable)
    for method in methods:
        plt.figure(figsize=(12, 6))
        for density in obstacle_densities:
            sizes = results[method][density]['sizes']
            turns = results[method][density]['turns']
            plt.plot(sizes, turns, marker='o', label=f'Density: {density}')
        plt.title(f'Minimal Number of Turns vs Grid Size - {method}')
        plt.xlabel('Grid Size (n)')
        plt.ylabel('Minimal Number of Turns')
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    main()
