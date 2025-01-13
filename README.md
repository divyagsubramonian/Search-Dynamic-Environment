# Search in Dynamic Environments

The foundation of Agent A’s movement is reliant on the flood fill algorithm, which utilizes BFS (breadth-first search). The code can be broken down into two core components or cases: (1) finding the path to the best coin and (2) finding the path to the goal. 

My code first defines the possible directions in which Agent A can move (W = up, A = left, S = down, and D = right). I omitted I = stay in place, as I wanted Agent A to always be moving towards a target, whether it be the goal or the best coin. I then store the current position in a global variable that tracks all the spots that have been visited. Afterwards, I find the position of the goal and the cost of travelling from the agent’s current position to the goal. The cost is calculated using the weighted Manhattan distance (where the penalty is factored in). 

After this, I calculate the expected gains from going to each coin. Essentially, I iterate through every coin, finding every neighboring coin that is within a given radius (5 / penalty_k) of the main coin and calculating the expected gain from going to the main coin (10 * number of coins in vicinity). Using the expected gain from each coin on the map, I find the best coin that the agent can travel to. The best coin is calculated by finding the weighted Manhattan distance between the current position and a given coin minus the expected gain of that coin.

After calculating the costs of going to the best coin and the goal, I branch into two cases. If the cost of going to the coin is less than the cost of going to the goal, I then find the shortest path from the current position to the coin using the flood fill algorithm. If the cost of going to the goal is less than the cost of going to the best coin, I find the shortest path from the current position to the goal using the flood fill algorithm.  

The flood fill algorithm populates a 50 x 30 map (corresponding to the coordinate map), where the coin locations are filled with zeros and walls are filled with 80s. A queue is set up, where the best coin (initial starting location) is the only position pushed onto the queue. Each item in the queue is a tuple containing the position and the value it is being filled with. I check that the neighbors of the position that is popped from the queue are valid and haven’t already been visited. If these conditions are satisfied, the neighbor is added to the queue, and its position is filled with a value one greater than its parent. This process is repeated until the queue is empty or the current position has been reached.

After I find the flood fill map (whether the target is the goal or the best coin), I find each possible neighboring position of the current position and use a priority queue to order the neighbors by their corresponding values on the flood fill map (in increasing order). I also factored in picking up nearby coins on the way to the target. This process somewhat models greedy best first search. Therefore, popping the first element from the priority queue will give us the most optimal action for the agent to take.

`manhattan_distance`: calculates the weighted manhattan distance between two points

`is_valid`: determines if a position is valid (within the map, not a wall, and not a car)

`expected_coin_gains`: calculates the expected gain for each coin cluster

`best_coin`: determines the best coin to go to based on the traveling cost and expected gain

`bfs`: populates a map that includes all the possible paths that can be taken (flood fill algorithm using BFS)
