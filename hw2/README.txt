**TASK:**
1. Implement the Q-Learning algorithm by adding a new function to the existing
codebase. The function should be named q_learning and should take as input a maze
object, the number of episodes, the learning rate (α), the discount factor (γ), and the
exploration rate (ε).
2. Create a function named q_learning_path that takes as input a maze object and a
learned Q-table, and returns the found path from the starting position to the goal
position, along with its cost.
3. Train the Q-Learning algorithm on the input maze. You should use the visualization
functions already provided in the codebase to create a visual representation of each
maze and the found paths.
4. Implement the Q-Learning-based maze traversal algorithm using the following
outline:
    a. Initialize the Q-Table with zeros and set values of parameters by yourself.
    b. Set the initial state (the starting position of the agent).
    c. Choose an action based on the current state and the Q-Table, using the ε-greedy
    strategy.
    d. Perform the action and observe the reward and the next state.
    e. Update the Q-Table using the Q-Learning update rule.
    f. Set the next state as the current state.
    g. Repeat steps c-f until the agent reaches the goal or a predefined maximum
    number of iterations is reached.
    f. You should use the visualization functions already provided in the codebase to
    create a visual representation of each maze and the found paths. Please
    demonstrates the algorithm's performance from the 3 randomly generated mazes.
5. Choose at least two parameters and change values of them to see the impact of the
parameters. (e.g., test the performance when (α=0.2, α=0.4, α=0.6, α=0.8) and (γ
=0.2, γ =0.4, γ =0.6, γ =0.8)). Discuss the impact of parameters in your report.
6. Write a detailed report that explains your implementation of the Q-Learning
algorithm, including any modifications or enhancements you made to the existing
codebase. 
