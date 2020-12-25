import networkx as nx

INPUT_FILE = "Day-6\input.txt"

def get_root_node(edges):
    graph = nx.DiGraph()
    for edge in edges:
        graph.add_edge(edge[0], edge[1])
    return list(nx.topological_sort(graph))[0]

def create_graph(edges):
    graph = nx.Graph()
    for edge in edges:
        graph.add_edge(edge[0], edge[1])
    return graph

def solve_part1(content):
    graph = create_graph(content)
    root = get_root_node(content)
    return sum([len(nx.shortest_path(graph, source=node, target=root)) - 1 for node in graph.nodes])

def solve_part2(content):
    graph = create_graph(content)
    return len(nx.shortest_path(graph, source='YOU', target='SAN')) - 3

def prepare_content(content):
    return [ (o.split(')')[0], o.split(')')[1]) for o in content]

def solve_puzzle(part, filename):
    with open(filename, 'r') as file:
        content = file.readlines()
        content = [x.strip() for x in content]
        content = prepare_content(content)
        if part == 1:
            return solve_part1(content)
        elif part == 2:
            return solve_part2(content)

def main():

    result = solve_puzzle(1, INPUT_FILE)
    print("part 1: {}".format(result))

    result = solve_puzzle(2, INPUT_FILE)
    print("part 2: {}".format(result))

if __name__ == '__main__':
	main()
