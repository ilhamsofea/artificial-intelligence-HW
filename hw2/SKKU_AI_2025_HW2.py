import pygame
import numpy as np
import random
import time
import sys
from collections import deque
import heapq

# Set fixed random seed for reproducibility
random.seed(88)
np.random.seed(55)

class MazeVisualizer:
    # Colors
    WHITE = (255, 255, 255)  # Path
    BLACK = (0, 0, 0)  # Wall
    BLUE = (100, 100, 255)  # Visited
    RED = (255, 0, 0)  # Current position
    GREEN = (0, 200, 0)  # Start
    YELLOW = (255, 255, 0)  # End
    GRAY = (200, 200, 200)  # Grid lines

    def __init__(self, size=20, cell_size=30):
        """Initialize maze of given size."""
        self.size = size
        self.cell_size = cell_size
        self.maze = np.zeros((size, size), dtype=int)
        self.start = None
        self.end = None

        # Screen size with legend area on the right
        self.legend_width = 200  # Width of legend area
        self.screen_width = size * cell_size + self.legend_width
        self.screen_height = size * cell_size
        self.screen = None

        # Initialize pygame
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 16)

    def generate_maze(self, wall_probability=0.3):
        """Generate a random maze with walls."""
        self.maze = np.random.choice([0, 1], size=(self.size, self.size),
                                     p=[1 - wall_probability, wall_probability])
        return self.maze

    def ensure_path_exists(self):
        """Ensure that at least one path exists from start to end."""
        # Reset walls between start and end if needed
        queue = deque([self.start])
        visited = {self.start}

        # Define possible moves (up, right, down, left)
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while queue:
            current = queue.popleft()

            if current == self.end:
                return True  # Path already exists

            for dy, dx in moves:
                ny, nx = current[0] + dy, current[1] + dx

                if (0 <= ny < self.size and
                        0 <= nx < self.size and
                        (ny, nx) not in visited):

                    if self.maze[ny, nx] == 0:  # If it's a path
                        visited.add((ny, nx))
                        queue.append((ny, nx))

        # If we get here, no path may exists. please change the random seed or size.

        return False

    def set_start_end(self, start=None, end=None):
        """Set start and end positions."""
        if start is None:
            # Find random valid start position
            valid_positions = list(zip(*np.where(self.maze == 0)))
            if not valid_positions:  # If no valid positions (all walls)
                self.maze[0, 0] = 0  # Make top-left corner a path
                self.start = (0, 0)
            else:
                self.start = random.choice(valid_positions)
        else:
            self.start = start
            self.maze[self.start] = 0  # Ensure start is walkable

        if end is None:
            # Find random valid end position that is different from start
            valid_positions = list(zip(*np.where(self.maze == 0)))
            if self.start in valid_positions:
                valid_positions.remove(self.start)

            if not valid_positions:  # If no other valid positions
                if self.start != (self.size - 1, self.size - 1):
                    self.end = (self.size - 1, self.size - 1)
                else:
                    self.end = (0, self.size - 1)
                self.maze[self.end] = 0  # Ensure end is walkable
            else:
                self.end = random.choice(valid_positions)
        else:
            self.end = end
            self.maze[self.end] = 0  # Ensure end is walkable

        # Ensure a path exists
        if not self.ensure_path_exists():
            print("no path may exists. please change the random seed or size.")
            exit()

        return self.start, self.end

    def setup_visualization(self):
        """Setup the visualization environment using pygame."""
        pygame.display.set_caption("DFS Maze Traversal")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

    def draw_maze(self, current=None, visited=None, path=None, show_path_line=False):
        """Draw the maze with pygame."""
        self.screen.fill(self.WHITE)

        # Draw cells
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                # Draw walls
                if self.maze[y, x] == 1:
                    pygame.draw.rect(self.screen, self.BLACK, rect)

                # Draw grid lines
                pygame.draw.rect(self.screen, self.GRAY, rect, 1)

        # Draw visited cells
        if visited:
            for y, x in visited:
                if (y, x) != self.start and (y, x) != self.end:
                    rect = pygame.Rect(
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size,
                        self.cell_size
                    )
                    pygame.draw.rect(self.screen, self.BLUE, rect)
                    pygame.draw.rect(self.screen, self.GRAY, rect, 1)

        # Draw final path
        if path:
            for y, x in path:
                if (y, x) != self.start and (y, x) != self.end:
                    rect = pygame.Rect(
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size,
                        self.cell_size
                    )
                    pygame.draw.rect(self.screen, self.BLUE, rect)
                    pygame.draw.rect(self.screen, self.GRAY, rect, 1)

            # Draw connected line through path if requested
            if show_path_line and len(path) > 1:
                points = []
                for y, x in path:
                    points.append((
                        x * self.cell_size + self.cell_size // 2,
                        y * self.cell_size + self.cell_size // 2
                    ))
                pygame.draw.lines(self.screen, (255, 165, 0), False, points, 4)  # Orange line

        # Draw current position
        if current and current != self.start and current != self.end:
            rect = pygame.Rect(
                current[1] * self.cell_size,
                current[0] * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(self.screen, self.RED, rect)
            pygame.draw.rect(self.screen, self.GRAY, rect, 1)

        # Draw start position with triangle
        start_center = (
            self.start[1] * self.cell_size + self.cell_size // 2,
            self.start[0] * self.cell_size + self.cell_size // 2
        )
        start_radius = self.cell_size // 2 - 4

        # Draw a green triangle for start
        points = [
            (start_center[0], start_center[1] - start_radius),
            (start_center[0] - start_radius, start_center[1] + start_radius),
            (start_center[0] + start_radius, start_center[1] + start_radius)
        ]
        pygame.draw.polygon(self.screen, self.GREEN, points)

        # Draw end position with circle
        end_center = (
            self.end[1] * self.cell_size + self.cell_size // 2,
            self.end[0] * self.cell_size + self.cell_size // 2
        )
        end_radius = self.cell_size // 2 - 4
        pygame.draw.circle(self.screen, self.YELLOW, end_center, end_radius)

        # Draw legend on the right side
        self.draw_legend()

        # Update display
        pygame.display.flip()

    def draw_legend(self):
        """Draw a legend explaining the colors on the right side."""
        # Legend area
        legend_x = self.size * self.cell_size + 20
        legend_y = 20
        legend_item_height = 40

        # Title
        title_text = self.font.render("LEGEND", True, self.BLACK)
        self.screen.blit(title_text, (legend_x, legend_y))
        legend_y += 30

        # Legend items - (color, label)
        legend_items = [
            (self.WHITE, "Path"),
            (self.BLACK, "Wall"),
            (self.BLUE, "Visited"),
            (self.RED, "Current"),
            (self.GREEN, "Start"),
            (self.YELLOW, "End"),
            ((255, 165, 0), "Final Path Line")
        ]

        for color, label in legend_items:
            # Color box
            pygame.draw.rect(
                self.screen,
                color,
                pygame.Rect(legend_x, legend_y, 30, 30)
            )
            pygame.draw.rect(
                self.screen,
                self.BLACK,
                pygame.Rect(legend_x, legend_y, 30, 30),
                1
            )

            # Label
            text = self.font.render(label, True, self.BLACK)
            self.screen.blit(text, (legend_x + 40, legend_y + 5))

            legend_y += legend_item_height

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def astar(self, delay=100):
        """Perform A* traversal and visualization."""
        if not self.start or not self.end:
            raise ValueError("Start and end positions must be set before traversal.")

        # Setup visualization
        if self.screen is None:
            self.setup_visualization()

        # A* variables
        open_cell = []
        heapq.heappush(open_cell, (0, self.start, [self.start])) # Priority queue for A* (cost, current, path)
        g_costs = {self.start: 0}  # Cost to reach each node
        visited = set()

        # Define possible moves (up, right, down, left)
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        path_found = False
        final_path = None
        total_cells_visited = 0

        # Print start of traversal to console
        print("\n----- A* Traversal Locations -----")
        print(f"Start position: {self.start}")

        # Main loop
        running = True
        while running and open_cell:
            # Handle events
            self.handle_events()

            # A* step
            current_cost, current, path = heapq.heappop(open_cell)
            total_cells_visited += 1

            # Print current position to console
            print(f"Visiting: {current}")

            # Update visualization
            self.draw_maze(current, visited)
            pygame.time.delay(delay)  # milliseconds

            # Check if reached the end
            if current == self.end:
                path_found = True
                final_path = path
                print(f"End position reached: {self.end}")
                break

            # Explore neighbors
            for dy, dx in moves:
                ny, nx = current[0] + dy, current[1] + dx
                neighbor = (ny, nx)

                # Calculate costs f(n) = g(n) + h(n)
                g_cost = g_costs[current] + 1  # Cost from start to neighbor
                h_cost = self.manhattan_dist(neighbor, self.end)
                f_cost = g_cost + h_cost

                # Check if valid move
                if (0 <= ny < self.size and
                        0 <= nx < self.size and
                        self.maze[ny, nx] == 0 and
                        neighbor not in visited):
                    
                    # New heap entry
                    entry = (f_cost, neighbor, path + [neighbor])

                    if neighbor not in g_costs:
                        # Encountering neighbor for the first time
                        g_costs[neighbor] = g_cost
                        heapq.heappush(open_cell, entry)
                    else:
                        # Existing neighbor case: check if this path is cheaper and update
                        if g_cost < g_costs[neighbor]:
                            g_costs[neighbor] = g_cost
                            heapq.heappush(open_cell, entry)

            visited.add(current)

        # Visualize final path if found
        if path_found:
            print("\n----- Path Found! -----")
            print("Final path from start to end:")
            for i, cell in enumerate(final_path):
                print(f"Step {i}: {cell}")
                self.handle_events()  # Check if user wants to quit
                self.draw_maze(cell, visited, final_path[:i + 1])
                pygame.time.delay(delay // 2)

            # Final view with complete path and connected line
            self.draw_maze(None, visited, final_path, True)  # Show path line

            # TODO Display path length and total cost on screen
            self.display_stats(len(final_path), total_cells_visited)

            # Keep final view until user closes
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        pygame.quit()
                        return final_path

                    # Also exit on key press
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                            waiting = False

                # Small delay to prevent CPU hogging
                pygame.time.delay(10)

            return final_path
        else:
            print("\n----- No Path Found -----")
            return None
    
    def manhattan_dist(self, current, goal):
        x1,y1 = current
        x2,y2 = goal
        dx, dy = abs(x1 - x2), abs(y1 - y2)
        dist = dx + dy
        return dist

    def display_stats(self, path_length, total_cells_visited):
        """Display statistics about the traversal and path on the screen."""
        # Stats area
        stats_x = self.size * self.cell_size + 20
        stats_y = self.screen_height - 120

        # Title
        title_text = self.font.render("STATISTICS", True, self.BLACK)
        self.screen.blit(title_text, (stats_x, stats_y))
        stats_y += 30

        # Stats items
        stats_items = [
            f"Path length: {path_length} steps",
            f"Total cost: {total_cells_visited} cells"
        ]

        for stat in stats_items:
            text = self.font.render(stat, True, self.BLACK)
            self.screen.blit(text, (stats_x, stats_y))
            stats_y += 25

        pygame.display.flip()

    def reset(self):
        """Reset the maze for a new run."""
        pygame.quit()
        self.screen = None
        self.maze = np.zeros((self.size, self.size), dtype=int)
        self.start = None
        self.end = None

    #--------------------- NEW FUNCTION ----------------------
    def get_reward(self, current_state, action, next_state):
        if next_state == self.end:
            return 100
        elif self.maze[next_state[0], next_state[1]] == 1:  # Hit a wall
            return -10 # Penalize hitting walls
        else:
            return -0.1  # Small negative reward for each step

    def is_valid_state(self, state):
        y, x = state
        return 0 <= y < self.size and 0 <= x < self.size

    def decide_action(self, state, q_table, epsilon):
        if random.random() < epsilon:
            return random.randint(0, 3)  # Explore
        else:
            # Exploit with some randomness if multiple actions have the same Q-value
            q_values = q_table[state[0], state[1]]
            max_q = np.max(q_values)
            best_actions = np.where(q_values == max_q)[0]
            return random.choice(best_actions)
        
    def handle_movement(self, current_state, action):
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        dy, dx = moves[action]
        next_state = (current_state[0] + dy, current_state[1] + dx)
        cost_increment = 0 # default value

        # Check for out-of-bounds or wall collision
        if not self.is_valid_state(next_state) or self.maze[next_state[0], next_state[1]] == 1:
            next_state = current_state # back to original
            cost_increment = 1  # Increment cost due to collision

        reward = self.get_reward(current_state, action, next_state)
        return next_state, reward, cost_increment

    def q_learning(self, num_episodes=100, learning_rate=0.3, discount_factor=0.9, exploration_rate=0.5,delay=3):
        q_table = np.zeros((self.size, self.size, 4))  # Q-table: (row, col, action)
        epsilon = exploration_rate

        # Define possible moves (up, right, down, left)
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        visited = set()
        total_cells_visited = 0

        if self.screen is None:
            self.setup_visualization()

        for episode in range(num_episodes):
            current_state = self.start
            terminate = False
            path = [self.start]
            total_reward = 0 # Track reward for the episode

            while not terminate:
                # Choose action
                action = self.decide_action(current_state, q_table, epsilon)

                # Take action and observe
                dy, dx = moves[action]
                next_state = (current_state[0] + dy, current_state[1] + dx)

                # Handle wall collisions: Stay in the same state if hitting a wall
                next_state, reward, _ = self.handle_movement(current_state, action) 
                total_reward += reward

                # Update Q-table
                current_q = q_table[current_state[0], current_state[1], action]
                best_next_q = np.max(q_table[next_state[0], next_state[1]])
                temp_diff = reward + discount_factor * best_next_q - current_q 
                q_table[current_state[0], current_state[1], action] += learning_rate * temp_diff

                # Visualize
                visited.add(current_state)
                self.draw_maze(current_state,visited,path)
                pygame.time.delay(delay) 

                # Move to the next state
                current_state = next_state
                path.append(current_state)
                total_cells_visited +=1

                # Check if done
                if current_state == self.end:
                    terminate = True
                    print(f"Episode {episode + 1}/{num_episodes}: Reached goal! Total reward: {total_reward:.2f}")
                self.handle_events()

            # Decay epsilon
            epsilon *= 0.95
            if epsilon < 0.01:
                epsilon = 0.01

        self.display_stats(len(path),total_cells_visited)
        return q_table

    def q_learning_path(self, q_table):
        current_state = self.start
        path = [current_state]
        cost = 0 # Total cost

        visited = set()

        while current_state != self.end:

            action = np.argmax(q_table[current_state[0], current_state[1]])
            next_state, _, cost_increment = self.handle_movement(current_state, action) 

            # Handle next state
            current_state = next_state
            cost += cost_increment 

            path.append(current_state) 
            cost += 1  

            visited.add(current_state) 
            self.draw_maze(current_state, visited, path, True) 
            self.handle_events() 

            # Basic loop break condition (prevent infinite loops)
            if len(path) > self.size * self.size * 2: 
                print("Path length exceeded.  Possible loop.") 
                break 

        return path, cost 
    #----------------------END OF NEW FUNCTIONS----------------------

def main():

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

    # ------------------ TO TEST ALGORITHM PERFORMANCE ------------------------------
    # cell_size = 30  # Pixel size of each cell
    # maze_size = 20  # 20x20 grid

    # learning_rates = [0.6]
    # discount_factors = [0.8]
    # wall_probabilities = [0.2,0.3,0.4]

    # for wall_prob in wall_probabilities:
    #   for learning_rate in learning_rates:
    #     for discount_factor in   discount_factors:
    #       maze_vis = MazeVisualizer(size=maze_size, cell_size=cell_size)
    #       maze_vis.generate_maze(wall_probability=wall_prob)
    #       start, end = maze_vis.set_start_end()

    #       print(f"Q-Learning with: wall_prob={wall_prob}, learning_rate={learning_rate}, discount_factor={discount_factor}")

    #       alpha = learning_rate
    #       gamma = discount_factor
    #       exploration_rate = 0.5
    #       q_table = maze_vis.q_learning(num_episodes=100, learning_rate=alpha, discount_factor=gamma, exploration_rate=exploration_rate, delay=1)

    #       path, cost = maze_vis.q_learning_path(q_table)

    #       print(f"Q-Learning Path: {path}")
    #       print(f"Q-Learning Path Cost: {cost}")

    #       waiting = True
    #       while waiting:
    #         for event in pygame.event.get():
    #           if event.type == pygame.QUIT:
    #             waiting = False
    #             pygame.quit()
    #             break  

if __name__ == "__main__":
    main()

