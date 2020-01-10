INPUT_FILE = "Day-8\input.txt"

def get_layers(pic, width, height):
    layers = []
    layer = []
    for i in range(0, len(pic), width):
        layer.append(pic[i:i+width])
        if len(layer) == height:
            layers.append(layer)
            layer = []
    return layers

def solve_part1(content):
    layers = get_layers(content, 25, 6)
    count = lambda l, c : sum([ x.count(c) for x in l])
    idx = min([(i, count(layer, '0')) for i, layer in enumerate(layers)], key = lambda t: t[1])[0]
    return count(layers[idx], '1') * count(layers[idx], '2')

def solve_part2(content):
    width = 25
    height = 6
    layers = get_layers(content, width, height)
    picture = [[None for _ in range(width)] for _ in range(height)]

    for i in range(height * width):
        x = i % width
        y = i % height
        for layer in enumerate(layers):
            if picture[y][x] == None or picture[y][x] == '2':
                picture[y][x] = " " if layer[1][y][x] == '0' else layer[1][y][x]

    for ab in picture:
        print(''.join(ab))
    return None

def prepare_content(content):
    return content[0]

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
    print(f"part 1: {result}")

    result = solve_puzzle(2, INPUT_FILE)
    print(f"part 2: {result}")

if __name__ == '__main__':
	main()
