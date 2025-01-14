import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from heapq import heappush, heappop

def get_neighbor_nodes(curr_node: tuple[int], unvisited_nodes: set[tuple[int]], border_size: int) -> set[tuple[int]]:
    '''
        Get a set of neighbor nodes of a current node in a grid with given border size which is part of a vertex queue.

        Arguments:
            curr_node (tuple[int]): The current node.
            unvisited_nodes (tuple[int]): The set of unvisited vertices.
            border_size (int): The border size of the quadratic grid.
        
        Returns:
            get_neighbor_nodes (set[tuple[int]]): A set of unvisited neighbors of the current node.
    '''
    # Get all unvisited neighbors
    neighbor_candidates = set()

    # Top neighbor candidate
    if curr_node[0] > 0:
        neighbor_candidates.add((curr_node[0]-1, curr_node[1]))

    # Right neighbor candidate
    if curr_node[1] < border_size-1:
        neighbor_candidates.add((curr_node[0], curr_node[1]+1))

    # Bottom neighbor candidate
    if curr_node[0] < border_size-1:
        neighbor_candidates.add((curr_node[0]+1, curr_node[1]))

    # Left neighbor candidate
    if curr_node[1] > 0:
        neighbor_candidates.add((curr_node[0], curr_node[1]-1))
    
    return {neighbor_candidate for neighbor_candidate in neighbor_candidates if neighbor_candidate in unvisited_nodes}

def naive_dijkstra(matrix: list[list[int]], source_node: tuple[int], target_node: tuple[int]) -> int:
    '''
        A naive implementation of Dijkstra's path finding algorithm.

        Arguments:
            matrix (list[list[int]]): The risk matrix containing the risk values for all nodes on the grid.
            source_node (tuple): The source node for the path finding.
            target_node (tuple): The target node for the path finding.
        
        Returns:
            distance_matrix[source][target]: The minimal risk associated with the path of minimal risk between the source and target node.
    '''
    # Initialize the distance matrix with +inf everywhere apart from the initial node
    distance_matrix = [ [float("Inf") for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    distance_matrix[source_node[0]][source_node[1]] = 0

    # Initially, the vertex queue, i.e. the queue of unvisited vertices, contains all vertices of the grid
    unvisited_nodes = set()
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            unvisited_nodes.add((row, col))
            
    # Initial empty vertex queue
    vertex_queue = set()

    # Visit every unvisited vertex and update the risk scores for the neighbors
    is_initial = True
    curr_node = source_node
    while len(unvisited_nodes) > 0:
 
        # Get the unvisited neighbors of the current node
        curr_neighbors = get_neighbor_nodes(curr_node, unvisited_nodes, len(matrix))

        # Update the risk value for each unvisited neighbor in case a new minimal value is found
        for curr_neighbor in curr_neighbors:
            # The initial node is visited without risk
            if is_initial:
                new_val = matrix[curr_neighbor[0]][curr_neighbor[1]]
            else:
                new_val = distance_matrix[curr_node[0]][curr_node[1]] + matrix[curr_neighbor[0]][curr_neighbor[1]]

            if new_val < distance_matrix[curr_neighbor[0]][curr_neighbor[1]]:
                distance_matrix[curr_neighbor[0]][curr_neighbor[1]] = new_val
                vertex_queue.add(curr_neighbor)

        # In case we reach the target node, we have found the minimal value for reaching it
        if curr_node == target_node:
            return distance_matrix[target_node[0]][target_node[1]]

        # Count the current node as visited, hence removing it from the vertex queue
        unvisited_nodes.remove(curr_node)
        if curr_node in vertex_queue:
            vertex_queue.remove(curr_node)
        
        # Visit the next unvisited node with the minimal risk value associated to it
        min_val = float("Inf")
        for pot_new_node in vertex_queue:
            if distance_matrix[pot_new_node[0]][pot_new_node[1]] < min_val:
                min_val = distance_matrix[pot_new_node[0]][pot_new_node[1]]
                curr_node = pot_new_node

        # After the first iteration, the initial node's risk value counts as well (important if it is ever visited again)
        is_initial = False

    return distance_matrix[target_node[0]][target_node[1]]

def dijkstra_with_heap_queue(matrix: list[list[int]], source_node: tuple[int], target_node: tuple[int]) -> int:
    '''
        An implementation of Dijkstra's path finding algorithm with a heap queue.

        Arguments:
            matrix (list[list[int]]): The risk matrix containing the risk values for all nodes on the grid.
            source_node (tuple): The source node for the path finding.
            target_node (tuple): The target node for the path finding.
        
        Returns:
            distance_matrix[source][target]: The minimal risk associated with the path of minimal risk between the source and target node.
    '''
    # Initialize the distance matrix with +inf everywhere apart from the initial node
    distance_matrix = [ [float("Inf") for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    distance_matrix[source_node[0]][source_node[1]] = 0

    # Initially, the vertex queue, i.e. the queue of unvisited vertices, contains all vertices of the grid
    unvisited_nodes = set()
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            unvisited_nodes.add((row, col))

    # Initial empty vertex queue
    vertex_queue = []

    # Visit every unvisited vertex and update the risk scores for the neighbors
    is_initial = True
    curr_node = source_node
    while len(unvisited_nodes) > 0:
 
        # Get the unvisited neighbors of the current node
        curr_neighbors = get_neighbor_nodes(curr_node, unvisited_nodes, len(matrix))

        # Update the risk value for each unvisited neighbor in case a new minimal value is found
        for curr_neighbor in curr_neighbors:
            # The initial node is visited without risk
            if is_initial:
                new_val = matrix[curr_neighbor[0]][curr_neighbor[1]]
            else:
                new_val = distance_matrix[curr_node[0]][curr_node[1]] + matrix[curr_neighbor[0]][curr_neighbor[1]]

            # In case we found a new minimal value for a neighbor, update the distance matrix and add this neighbor to the queue
            if new_val < distance_matrix[curr_neighbor[0]][curr_neighbor[1]]:
                distance_matrix[curr_neighbor[0]][curr_neighbor[1]] = new_val
                heappush(vertex_queue, (new_val, curr_neighbor))

        # In case we reach the target node, we have found the minimal value for reaching it
        if curr_node == target_node:
            return distance_matrix[target_node[0]][target_node[1]]

        # Count the current node as visited, hence removing it from the vertex queue
        unvisited_nodes.remove(curr_node)
        
        # Visit the next unvisited node with the minimal risk value associated to it
        curr_node = heappop(vertex_queue)[1]

        # After the first iteration, the initial node's risk value counts as well (important if it is ever visited again)
        is_initial = False

    return distance_matrix[target_node[0]][target_node[1]]


# Solution to part 1
def part_1():
    result = 0

    risk_matrix = [[int(i) for i in row] for row in data_lines]
    result = naive_dijkstra(risk_matrix, (0,0), (len(risk_matrix)-1,len(risk_matrix)-1))

    return result

# Solution to part 2
def part_2():
    result = 0
    
    risk_matrix = [[int(i) for i in row] for row in data_lines]

    new_risk_matrix = []
    for curr_row in risk_matrix:
        new_row = []
        for i in range(5):
            new_row += [ sum( [int(k) for k in str(j+i)] ) for j in curr_row ]
        new_risk_matrix.append(new_row)
    intermediate_matrix = new_risk_matrix.copy()
    for i in range(1, 5):
        for m in range(len(intermediate_matrix)):
            new_row = [ sum( [int(k) for k in str(j+i)] ) for j in intermediate_matrix[m] ]
            new_risk_matrix.append(new_row)

    result = dijkstra_with_heap_queue(new_risk_matrix, (0,0), (len(new_risk_matrix)-1,len(new_risk_matrix)-1))

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
