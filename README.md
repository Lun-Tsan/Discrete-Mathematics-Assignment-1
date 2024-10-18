# Best Path Finder with Least Turns

This repository provides Python scripts and an HTML file for exploring pathfinding algorithms in a grid with obstacles. The goal is to find the best paths (with the least number of turns) in an \(n \times n\) grid.

## How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run All Scripts**:
   ```bash
   python3 main.py
   ```
   This will execute all scripts and save plots in the `result_images` folder.

## Requirements

- Python 3.x
- **NumPy**: For numerical computations
- **Matplotlib**: For plotting results

Install using:
```bash
pip install -r requirements.txt
```

## Files

- **Python Scripts**:
  - `possible_path.py`: Simulates and plots the number of possible paths with obstacles.
  - `best_path_trend.py`: Analyzes and plots trends for the number of best paths.
  - `best_path_count.py`: Count the number of best paths with obstacles.
  - `avg_turn.py`: Calculates and plots average turns in best paths.
  - `algo_compare.py`: Compares algorithms (Recursive, Dynamic Programming, Combinatorial, Dijkstra).
  - `main.py`: Runs all the above scripts.

- **HTML Visualization**:
  - `visualize.html`: Interactive visualization for finding the best path in an \(n \times n\) grid.

- **Output Folder**:
  - `result_images/`: Stores generated plots from each script.

-**Report**:
  - `report.pdf` : Report file.
