alpha = learning_rate
    gamma = discount_factor
    q_table = maze_vis.q_learning(num_episodes=100, learning_rate=alpha, discount_factor=gamma, exploration_rate=0.5,delay=3)