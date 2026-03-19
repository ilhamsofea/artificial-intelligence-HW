# Q-Learning Maze Solver

This project implements the Q-Learning algorithm to solve mazes. It uses Pygame for visualization.

## Dependencies

Before running the code, make sure you have the following dependencies installed:

*   **Python 3.x**
*   **Pygame:** Used for maze visualization. Install using pip:
    ```bash
    pip install pygame
    ```
*   **NumPy:** Used for numerical operations. Install using pip:
    ```bash
    pip install numpy
    ```
## Running the Code

The `SKKU_AI_HW2.py` file contains two primary ways to run the code, which are toggled using code comments:

**Option 1: Testing Parameter Combinations (Default)**

This configuration allows you to run the Q-Learning algorithm with a *single* specified parameter combination (wall probability, learning rate, discount factor) and observe the visualization.

1.  **Ensure this section in `SKKU_AI_2025_HW2.py` is uncommented:**

    ```python
        # ------------------- TO TEST PARAMETER COMBINATIONS ------------------------------
        # comb: lr=0.9 & df=0.2,0.4,0.8, lr=0.3 & df=0.2(X),0.4(X),0.8, lr= 0.6 & df=0.2,0.4,0.8
        # Create maze
        cell_size = 30  # Pixel size of each cell
        maze_size = 20  # 20x20 grid
        maze_vis = MazeVisualizer(size=maze_size, cell_size=cell_size)
        wall_probability = 0.3
        learning_rate=0.6
        discount_factor=0.8

        # Generate maze (for param combination)
        maze_vis.generate_maze(wall_probability=0.3)
        start, end = maze_vis.set_start_end()
        print(f"Q-Learning with: wall_prob={wall_probability}, learning_rate={learning_rate}, discount_factor={discount_factor}")

        alpha = learning_rate
        gamma = discount_factor
        q_table = maze_vis.q_learning(num_episodes=100, learning_rate=alpha, discount_factor=gamma, exploration_rate=0.5,delay=3)

        # Extract and visualize the path
        path, cost = maze_vis.q_learning_path(q_table)

        print(f"Q-Learning Path: {path}")
        print(f"Q-Learning Path Cost: {cost}")

        # Keep the window open until the user closes it
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    break  # Exit the inner loop and the main loop
    ```

2.  **Customize parameters:** Modify the `wall_probability`, `learning_rate`, and `discount_factor` variables within this section to test different combinations.

3.  **Run the script:**
    *   **Using a terminal or command prompt:**
        ```bash
        python SKKU_AI_2025_HW2.py
        ```
    *   **In Visual Studio Code:** Open `SKKU_AI_2025_HW2.py` and simply click the "Run" button (usually a green triangle) at the top of the editor or use the debugger.

4.  **Observe the visualization:** The Pygame window will display the maze, the path the algorithm is taking and any other relevant informations.

**Option 2: Testing Algorithm Performance across Multiple Mazes**

This configuration runs the Q-Learning algorithm across a set of pre-defined wall probabilities, learning rates, and discount factors. This setting is useful for observing the algorithm performance across different maze and parameter combinations.

1.  **Comment out the "Testing Parameter Combinations" section:**
    ```python
    # ------------------- TO TEST PARAMETER COMBINATIONS ------------------------------
    # (Comment out the entire section)
    # ...
    ```

2.  **Uncomment the "Testing Algorithm Performance" section:**
    ```python
        # ------------------ TO TEST ALGORITHM PERFORMANCE ------------------------------
        cell_size = 30  # Pixel size of each cell
        maze_size = 20  # 20x20 grid

        learning_rates = [0.6]
        discount_factors = [0.8]
        wall_probabilities = [0.2,0.3,0.4]

        for wall_prob in wall_probabilities:
          for learning_rate in learning_rates:
            for discount_factor in   discount_factors:
              maze_vis = MazeVisualizer(size=maze_size, cell_size=cell_size)
              maze_vis.generate_maze(wall_probability=wall_prob)
              start, end = maze_vis.set_start_end()

              print(f"Q-Learning with: wall_prob={wall_prob}, learning_rate={learning_rate}, discount_factor={discount_factor}")

              alpha = learning_rate
              gamma = discount_factor
              exploration_rate = 0.5
              q_table = maze_vis.q_learning(num_episodes=100, learning_rate=alpha, discount_factor=gamma, exploration_rate=exploration_rate, delay=1)

              path, cost = maze_vis.q_learning_path(q_table)

              print(f"Q-Learning Path: {path}")
              print(f"Q-Learning Path Cost: {cost}")

              waiting = True
              while waiting:
                for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    break
    ```

3.  **Customize the parameters**: Modify the lists `learning_rates`, `discount_factors`, and `wall_probabilities` to specify the parameter combinations you want to test.

4.  **Run the script:**
    *   **Using a terminal or command prompt:**
        ```bash
        python SKKU_AI_2025_HW2.py
        ```
    *   **In Visual Studio Code:** Open `SKKU_AI_2025_HW2.py` and simply click the "Run" button (usually a green triangle) at the top of the editor or use the debugger.

5.  **Observe the visualizations and console output:** For each combination of parameters, the program will output the path found and the cost. A Pygame window is also opened to visualize the path, and will remain open until closed.

## Code Structure

*   `SKKU_AI_2025_HW2.py`: Contains the main code for running the Q-Learning algorithm and visualizing the maze.
*   `MazeVisualizer` class: Implements the maze generation, visualization, and Q-Learning algorithm.

## Notes

*   Ensure that the correct section is uncommented depending on the desired testing approach.
*   Adjust the `delay` parameter within the `q_learning` function to control the speed of visualization (lower values result in faster visualization).
*   If the program outputs "no path may exists. please change the random seed or size.", it may indicates that a path from the start to the end does not exists with the current random seed or maze size. To mitigate this, try increasing the maze size or experiment with multiple random seeds.
