# **Best Path Finder with Least Turns**

This repository contains a collection of Python scripts and an HTML file that explore pathfinding algorithms in a grid with obstacles. The main focus is on finding the best paths (with the least number of turns) from the top-left corner to the bottom-right corner in an \( n \times n \) grid. The repository includes:

- **Python Scripts**:
  - `possible_path.py`: Simulates and plots the average number of possible paths in grids with varying obstacle densities.
  - `best_path_trend.py`: Analyzes and plots the trend of the number of best paths with minimal turns.
  - `avg_turn.py`: Simulates and plots the average number of turns in the best paths for different grid sizes and obstacle densities.
  - `algo_compare.py`: Compares different algorithms (Recursive, Dynamic Programming, Combinatorial) in terms of execution time, number of paths, and minimal number of turns.
  - `main.py`: Executes all the above scripts sequentially.
- **HTML Visualization**:
  - `grid_visualization.html`: An interactive web page that allows you to visualize the grid, place obstacles, and find the best path with the least number of turns.

All generated images are saved in the `result_images` folder.

---

## **Table of Contents**

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Scripts](#running-the-scripts)
  - [Running All Scripts](#running-all-scripts)
  - [Running Individual Scripts](#running-individual-scripts)
- [Viewing the HTML Visualization](#viewing-the-html-visualization)
- [Scripts Description](#scripts-description)
  - [possible_path.py](#possible_pathpy)
  - [best_path_trend.py](#best_path_trendpy)
  - [avg_turn.py](#avg_turnpy)
  - [algo_compare.py](#algo_comparepy)
  - [main.py](#mainpy)
- [Results](#results)
- [Dependencies](#dependencies)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## **Project Overview**

The project explores pathfinding in grids with obstacles, focusing on finding the best paths with the least number of turns. It compares different algorithms and visualizes the results through plots and an interactive HTML grid.

---

## **Prerequisites**

- **Python 3.x**: Ensure you have Python 3 installed on your system.
- **pip**: Python package manager to install dependencies.
- **Web Browser**: To view the HTML visualization (e.g., Chrome, Firefox, Safari).

---

## **Installation**

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your_username/best-path-finder.git
   cd best-path-finder
   ```

2. **Create a Virtual Environment** (Optional but recommended):

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:

   - **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` file includes:

   ```txt
   numpy
   matplotlib
   ```

---

## **Running the Scripts**

### **Running All Scripts**

To run all the scripts sequentially and generate all plots:

```bash
python main.py
```

This will execute the main functions from each script and save the generated images in the `result_images` folder.

### **Running Individual Scripts**

You can also run each script individually:

- **possible_path.py**:

  ```bash
  python possible_path.py
  ```

- **best_path_trend.py**:

  ```bash
  python best_path_trend.py
  ```

- **avg_turn.py**:

  ```bash
  python avg_turn.py
  ```

- **algo_compare.py**:

  ```bash
  python algo_compare.py
  ```

Note: If you run the scripts individually, make sure to uncomment the execution block at the bottom of each script:

```python
if __name__ == "__main__":
    main_function_name()
```

---

## **Viewing the HTML Visualization**

To view the interactive grid visualization:

1. **Open the HTML File**:

   - Locate the `grid_visualization.html` file in the repository.
   - Open it using a web browser.

2. **Usage Instructions**:

   - **Grid Size**: Enter a positive integer for the grid size \( n \).
   - **Obstacle Density**: Enter a value between 0 and 1 for the obstacle density.
   - **Find Best Path**: Click the "Find Best Path" button to generate the grid and find the best path.
   - **Reset Grid**: Click the "Reset Grid" button to reset the inputs and clear the grid.

---

## **Scripts Description**

### **possible_path.py**

- **Purpose**: Simulates the number of possible paths from the start to the end in grids with varying sizes and obstacle densities.
- **Functionality**:
  - Generates grids with obstacles based on specified densities.
  - Calculates the average number of possible paths over multiple simulations.
  - Plots the results on a logarithmic scale.
- **Output**: Saves `possible_paths.png` in the `result_images` folder.

### **best_path_trend.py**

- **Purpose**: Analyzes and plots the trend of the number of best paths with minimal turns as the grid size increases.
- **Functionality**:
  - Calculates the number of paths with exactly \( t \) turns using combinatorial methods.
  - Plots the number of best paths for minimal turns (1 turn) and minimal turns plus one (2 turns).
- **Output**: Saves `best_path_trend.png` in the `result_images` folder.

### **avg_turn.py**

- **Purpose**: Simulates and plots the average number of turns in the best paths for different grid sizes and obstacle densities.
- **Functionality**:
  - Generates grids with obstacles.
  - Finds the best path with the least number of turns using BFS.
  - Calculates the average number of turns over multiple simulations.
  - Plots the results.
- **Output**: Saves `average_turns.png` in the `result_images` folder.

### **algo_compare.py**

- **Purpose**: Compares different algorithms (Recursive, Dynamic Programming, Combinatorial) in terms of execution time, number of paths, and minimal number of turns.
- **Functionality**:
  - Implements three methods to find the best paths:
    - Recursive Method
    - Dynamic Programming Method
    - Combinatorial Method
  - Measures execution time for each method.
  - Plots execution times, number of paths, and minimal turns.
- **Output**: Saves multiple images in the `result_images` folder:
  - Execution time plots: `execution_time_*.png`
  - Number of paths plots: `number_of_paths_*.png`
  - Minimal turns plots: `minimal_turns_*.png`

### **main.py**

- **Purpose**: Runs all the above scripts sequentially.
- **Functionality**:
  - Imports and executes the main functions from each script.
  - Ensures that all results are generated and saved.

---

## **Results**

All generated images are saved in the `result_images` folder:

- **Possible Paths Plot**: `possible_paths.png`
- **Best Path Trend Plot**: `best_path_trend.png`
- **Average Turns Plot**: `average_turns.png`
- **Algorithm Comparison Plots**:
  - Execution Time: `execution_time_*.png`
  - Number of Paths: `number_of_paths_*.png`
  - Minimal Turns: `minimal_turns_*.png`

---

## **Dependencies**

The project requires the following Python packages:

- **NumPy**: For numerical computations and array handling.
- **Matplotlib**: For plotting graphs and saving figures.

These can be installed using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**

- Thanks to everyone who contributed to the development of these scripts.
- The HTML visualization was inspired by interactive pathfinding projects and aims to provide a user-friendly interface for exploring the algorithms.

---

## **Additional Notes**

- **Random Seed**: A fixed random seed (`11505050`) is used in the scripts to ensure reproducibility.
- **Simulations Per Point**: The number of simulations per data point is set to high values for accuracy (e.g., `1000`, `10000`). Adjust these values in the scripts if you need faster execution.
- **Recursion Limit**: The recursion limit is increased in `algo_compare.py` to handle deeper recursive calls:

  ```python
  sys.setrecursionlimit(1000000)
  ```

  Be cautious with memory usage when running recursive algorithms on large grids.

- **Virtual Environment**: It's recommended to use a virtual environment to manage dependencies and avoid conflicts with other Python projects.

---

## **Contact**

If you have any questions, suggestions, or issues, please feel free to open an issue or contact the repository owner.

