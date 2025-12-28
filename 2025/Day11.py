import sys
sys.path.append('..')
from Driver import load_data
part, input_type, data_raw, data_lines, data_lines_int = load_data()

from collections import defaultdict

def get_forward_connections(data_lines):
    connections = {}

    for line in data_lines:
        source, targets = line.split(': ')
        targets = targets.split()

        connections[source] = targets
    
    return connections

def get_backward_connections(forward_connections):
    backward_connections = defaultdict(list)

    for source_node, target_nodes in forward_connections.items():
        for target_node in target_nodes:
            backward_connections[target_node].append(source_node)

    return backward_connections

def check_connectivity(start_node, connections):
    connected_to = set([start_node])
    next_nodes = set([start_node])

    while len(next_nodes) > 0:
        new_nodes = set()
        
        for next_node in next_nodes:
            new_nodes.update(set(connections[next_node]))

        connected_to.update(new_nodes)

        if 'out' in new_nodes:
            new_nodes.remove('out')

        next_nodes = new_nodes.copy()

    return connected_to

def filter_connections(forward_connections, filter_set):
    filtered_connections = defaultdict(list)

    for source, targets in forward_connections.items():
        if source not in filter_set:
            continue
        
        for target in targets:
            if target not in filter_set:
                continue

            filtered_connections[source].append(target)
    
    return filtered_connections

def get_all_paths(source, target, connections):
    final_paths = []
    current_paths = [[source]]

    while len(current_paths) > 0:
        next_paths = []

        for current_path in current_paths:
            next_node_candidates = connections[current_path[-1]]

            for next_node_candidate in next_node_candidates:
                if next_node_candidate == target:
                    final_paths.append(current_path + [next_node_candidate])
                    continue

                if next_node_candidate in current_path:
                    continue

                next_paths.append(current_path + [next_node_candidate])

        current_paths = next_paths[:]
    
    return final_paths

# Solution to part 1
def part_1():
    forward_connections = get_forward_connections(data_lines)
    final_paths = get_all_paths('you', 'out', forward_connections)

    return len(final_paths)

# Solution to part 2
def part_2():
    forward_connections = get_forward_connections(data_lines)
    backward_connections = get_backward_connections(forward_connections)

    forward_reachable = defaultdict(set)
    backward_reachable = defaultdict(set)

    forward_reachable['svr'] = check_connectivity('svr', forward_connections)
    forward_reachable['fft'] = check_connectivity('fft', forward_connections)
    forward_reachable['dac'] = check_connectivity('dac', forward_connections)

    backward_reachable['out'] = check_connectivity('out', backward_connections)
    backward_reachable['fft'] = check_connectivity('fft', backward_connections)
    backward_reachable['dac'] = check_connectivity('dac', backward_connections)


    filtered_connections = {
        'svr_to_fft': filter_connections(forward_connections, forward_reachable['svr'] & backward_reachable['fft']),
        'fft_to_dac': filter_connections(forward_connections, forward_reachable['fft'] & backward_reachable['dac']),
        'dac_to_out': filter_connections(forward_connections, forward_reachable['dac'] & backward_reachable['out'])
    }

    final_paths = {
        'svr_to_fft': get_all_paths('svr', 'fft', filtered_connections['svr_to_fft']),
        'fft_to_dac': get_all_paths('fft', 'dac', filtered_connections['fft_to_dac']),
        'dac_to_out': get_all_paths('dac', 'out', filtered_connections['dac_to_out'])
    }
    
    return len(final_paths['svr_to_fft'])*len(final_paths['fft_to_dac'])*len(final_paths['dac_to_out'])

# Print the result
if part == 1:
    print(part_1())
elif part == 2:
    print(part_2())
