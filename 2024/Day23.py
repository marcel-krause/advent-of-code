import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def get_all_nodes_and_edges(data_lines):
    nodes = defaultdict(set)

    for line in data_lines:
        node1, node2 = line.split('-')
        nodes[node1].add(node2)
        nodes[node2].add(node1)

    return nodes

def get_trios(nodes, only_t_trios=True):
    node_queue = list(nodes.keys())
    checked_trios = set()

    for i in range(len(node_queue)-1):
        node1 = node_queue[i]
        for node2 in nodes[node1]:
            pair_nodes = nodes[node1].intersection(nodes[node2])

            for pair_node in pair_nodes:
                trio = tuple(sorted([node1, node2, pair_node]))

                if only_t_trios and (trio[0][0] != 't' and trio[1][0] != 't' and trio[2][0] != 't'):
                    continue

                if len(nodes[pair_node].intersection({node1, node2})) >= 2 and trio not in checked_trios:
                    checked_trios.add(trio)
    
    return checked_trios

def get_n_tuples(nodes, tuples, n):
    n_tuples = set()

    for current_tuple in tuples[n-1]:
        node_intersection = nodes[current_tuple[0]].copy()

        for intersection_node in current_tuple[1:]:
            node_intersection = node_intersection.intersection(nodes[intersection_node])

        for new_node in node_intersection:
            n_tuples.add(tuple(sorted(list(current_tuple) + [new_node])))
    
    return n_tuples


# Solution to part 1
def part_1():
    result = 0

    nodes = get_all_nodes_and_edges(data_lines)
    result = len(get_trios(nodes, only_t_trios=True))

    return result

# Solution to part 2
def part_2():
    result = 0

    nodes = get_all_nodes_and_edges(data_lines)
    n_tuples = {3: get_trios(nodes, only_t_trios=False)}

    n = 4
    while True:
        n_tuples[n] = get_n_tuples(nodes, n_tuples, n)

        if len(n_tuples[n]) == 0:
            break

        n += 1

    maximum_clique = n_tuples[n-1].pop()
    result = ','.join(maximum_clique)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
