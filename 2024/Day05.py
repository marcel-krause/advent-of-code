import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(G):
    plt.figure(figsize =(9, 9)) 
    nx.draw_networkx(G, with_labels = True, node_color ='cyan') 
    plt.show()

def get_graph_configurations(data_lines):
    node_connections = []
    node_list = set()
    updates = []
    for line in data_lines:
        if "|" in line:
            node_connection = tuple(map(lambda x: int(x), line.split("|")))
            node_connections.append(node_connection)
            node_list.add(node_connection[0])
            node_list.add(node_connection[1])
        elif "," in line:
            updates.append(list(map(lambda x: int(x), line.split(","))))
    return node_connections, node_list, updates

def apply_updates(G, updates, node_list, correct_order=False):
    result = 0
    for update in updates:
        relevant_nodes = set(update)
        irrelevant_nodes = node_list.difference(relevant_nodes)

        H = G.copy()
        H.remove_nodes_from(irrelevant_nodes)
        topological_sort = list(nx.topological_sort(H))

        if correct_order:
            if topological_sort == update:
                result += update[len(update)//2]
        else:
            if topological_sort != update:
                result += topological_sort[len(update)//2]

    return result

# Solution to part 1
def part_1():
    result = 0

    node_connections, node_list, updates = get_graph_configurations(data_lines)
    
    G = nx.DiGraph()
    G.add_edges_from(node_connections)

    result = apply_updates(G, updates, node_list, correct_order=True)

    return result

# Solution to part 2
def part_2():
    result = 0

    node_connections, node_list, updates = get_graph_configurations(data_lines)
    
    G = nx.DiGraph()
    G.add_edges_from(node_connections)

    result = apply_updates(G, updates, node_list, correct_order=False)

    return result

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
