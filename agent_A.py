from collections import deque

discovered = []
# target_coin = None

# -*- coding: utf-8 -*-
def logic_A(cur_map, cur_position, cur_coins, cur_car_positions, penalty_k):
    # W = up, A = left, S = down, D = right, I = stay
    directions = [('W', 0, -1),
                  ('A', -1, 0),
                  ('S', 0, 1),
                  ('D', 1, 0)]
    
    # Current position (x, y)
    x, y = cur_position
    discovered.append((x, y))

    # Goal position (goal_x, goal_y)
    goal_x, goal_y = None, None
    goal_dist = None

    # Find goal node coordinates
    for row in range(len(cur_map)):
        for col in range(len(cur_map[0])):
            if cur_map[row][col] == 'goal':
                goal_x = row
                goal_y = col
                break

    # Find goal cost and best coin
    goal_dist = manhattan_distance(cur_position, (goal_x, goal_y), penalty_k)
    expected_gains = expected_coin_gains(cur_coins, penalty_k)
    best, coin_cost = best_coin(cur_position, cur_coins, penalty_k, expected_gains)

    # If best coin cost is better than goal cost
    if (coin_cost < goal_dist):
        path_map = bfs(cur_position, best, cur_map, cur_coins, cur_car_positions, directions)

        f_scores = []
        for item in directions:
            neighbor = (x + item[1], y + item[2])
            
            if not is_valid(neighbor, cur_map, cur_car_positions) and (neighbor not in discovered):
                continue

            if neighbor in cur_coins:
                return item[0]
                        
            cur_to_coin_dist = path_map[neighbor[0]][neighbor[1]]

            f_scores.append((item[0], cur_to_coin_dist))
        
        return min(f_scores, key=lambda tup: tup[1])[0]
    
    # If goal cost is better than best coin cost
    else:
        path_map = bfs(cur_position, (goal_x, goal_y), cur_map, cur_coins, cur_car_positions, directions)

        f_scores = []
        for item in directions:
            neighbor = (x + item[1], y + item[2])
            
            if not is_valid(neighbor, cur_map, cur_car_positions) and (neighbor not in discovered):
                continue

            if neighbor in cur_coins:
                return item[0]
                        
            cur_to_coin_dist = path_map[neighbor[0]][neighbor[1]]

            f_scores.append((item[0], cur_to_coin_dist))
        
        return min(f_scores, key=lambda tup: tup[1])[0]


### HELPER FUNCTIONS ###

# Calculates the weighted manhattan distance between two points
def manhattan_distance(src_point, dest_point, penalty_k):
    return (abs(src_point[0] - dest_point[0]) + abs(src_point[1] - dest_point[1])) * penalty_k

# Determines if a position is valid
def is_valid(position, cur_map, cur_car_positions):
    x = position[0]
    y = position[1]

    return (0 <= x < len(cur_map) and
            0 <= y < len(cur_map[0]) and
            cur_map[x][y] != 'wall' and
            (x, y) not in cur_car_positions)

# Calculates the expected gain for each coin cluster
def expected_coin_gains(cur_coins, penalty_k):
    expected_gains = {}

    # radius = round(5 / penalty_k)
    radius = round(4 / penalty_k)

    for coin in cur_coins:
        coin_cluster = []

        for neighbor_coin in cur_coins:
            dist = abs(coin[0] - neighbor_coin[0]) + abs(coin[1] - neighbor_coin[1])

            if (dist > 0) and (dist <= radius):
                coin_cluster.append(neighbor_coin)
        
        expected_gain = 10 * len(coin_cluster)
        expected_gains[coin] = expected_gain
    
    return expected_gains

# Determines the best coin to go to based on the traveling cost and expected gain
def best_coin(cur_position, cur_coins, penalty_k, expected_gains):
    min_cost = float('inf')
    best = None

    for coin in cur_coins:
        dist = manhattan_distance(cur_position, coin, penalty_k)
        cost = (2 * dist) - expected_gains[coin]

        if cost < min_cost:
            min_cost = cost
            best = coin
    
    return best, min_cost

# Populates a map that includes all the possible paths that can be taken (floodfill algorithm using BFS)
def bfs(cur_position, best, cur_map, cur_coins, cur_car_positions, directions):
    path_map = [[80] * 30 for _ in range(50)] 
    queue = deque()
    visited = []
    count = 1

    for coin in cur_coins:
        path_map[coin[0]][coin[1]] = 0

    queue.append((best, 0))
    while queue and (cur_position not in visited):
        position, count = queue.popleft()

        if position not in visited:
            visited.append(position)
            path_map[position[0]][position[1]] = min(count, path_map[position[0]][position[1]])
                
            for item in directions:
                neighbor = (position[0] + item[1], position[1] + item[2])

                if not is_valid(neighbor, cur_map, cur_car_positions):
                    continue

                if neighbor not in visited:
                    queue.append((neighbor, count + 1))

    return path_map