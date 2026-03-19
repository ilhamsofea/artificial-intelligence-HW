####################################
# SKKU Introduction to AI class
# release date: 2025.03.12
# HW#1
# Your name: Sofea
# Student ID: 2022313292
####################################
    # 1) How A* differs: A* is an informed search algorithm which means that it takes into account the position of the goal
    # while searching for it and hence it searches quite a few nodes to reach to the goal. The search towards the goal
    # is guided by a heuristic function.
    # 2) Role of heuristic: Improves the search efficiency by prioritizing paths that are likely to be closer to the goal.
    # 3) How choice of heuristic affects A* performance: Heuristic functions help to find the shortest path by exploring the
    # least number of nodes possible. A heuristic should have properties like admissibility (if it never overestimates the cost 
    # of reaching goal) and consistency (if the estimated cost from current node to the goal is always less than or equal to the 
    # estimated cost from any adjacent node plus the step cost from current node to adjacent node). Commonly, Manhattan distance
    # and Euclidean distance are used as heuristics where the Manhattan distance is used for grid-based maps while Euclidean distance 
    # is used for direct point-to-point distance measurement.
    # 4) Time and space complexity advantage/disadvantage of A* compared to DFS:
    # ADVANTAGE: Finds optimal path if heuristic is admissible and can be much faster than DFS in most scenarios.
    # DISADVANTAGE: Higher space complexity compared to DFS and can be computationally expensive in very large spaces. #

    # TODO change this function for A-star search
    ########## submit this function only for HW#1 ##############################
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