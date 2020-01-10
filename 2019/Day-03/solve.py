import sys

INPUT_FILE = "Day-3\input.txt"

def get_size(wire, p, m):
    max_size = 0
    min_size = 0
    size = 0
    for w in wire:
        if w[0] == p:
            size += w[1]
        elif w[0] == m:
            size -= w[1]
        if size > max_size:
            max_size = size
        elif size < min_size:
            min_size = size
    return abs(min_size), abs(min_size) + max_size

def solve_part1(content):
    start_y, height = get_size(content[0], 'D', 'U')
    start_x, width = get_size(content[0], 'R', 'L')
    matrix = [ [ False for i in range(width + 1) ] for j in range(height + 1) ]
    matrix[start_y][start_x] = True
    x = start_x
    y = start_y
    for c in content[0]:
        for _ in range(c[1]):
            if c[0] == 'U':
                y -= 1
            elif c[0] == 'D':
                y += 1
            elif c[0] == 'R':
                x += 1
            elif c[0] == 'L':
                x -= 1
            matrix[y][x] = True    
    x = start_x
    y = start_y
    min_dist = height + width
    for c in content[1]:
        for _ in range(c[1]):
            if c[0] == 'U':
                y -= 1
            elif c[0] == 'D':
                y += 1
            elif c[0] == 'R':
                x += 1
            elif c[0] == 'L':
                x -= 1
            if y >= 0 and y < height and x >= 0 and x < width and matrix[y][x]:
                dist = abs(x - start_x) + abs(y - start_y)
                if dist < min_dist:
                    min_dist = dist
    return min_dist


def solve_part2(content):
    start_y, height = get_size(content[0], 'D', 'U')
    start_x, width = get_size(content[0], 'R', 'L')
    matrix = [ [ [False, 0] for i in range(width + 1) ] for j in range(height + 1) ]
    matrix[start_y][start_x][0] = True
    x = start_x
    y = start_y
    steps = 0
    for c in content[0]:
        for _ in range(c[1]):
            steps += 1
            if c[0] == 'U':
                y -= 1
            elif c[0] == 'D':
                y += 1
            elif c[0] == 'R':
                x += 1
            elif c[0] == 'L':
                x -= 1
            matrix[y][x][0] = True
            matrix[y][x][1] = steps
    
    x = start_x
    y = start_y
    best_steps = sys.maxsize
    steps = 0
    for c in content[1]:
        for _ in range(c[1]):
            steps += 1
            if c[0] == 'U':
                y -= 1
            elif c[0] == 'D':
                y += 1
            elif c[0] == 'R':
                x += 1
            elif c[0] == 'L':
                x -= 1
            if y >= 0 and y < height and x >= 0 and x < width and matrix[y][x][0]:
                s = steps + matrix[y][x][1]
                if s < best_steps:
                    best_steps = s
    return best_steps

def prepare_content(content):
    return [format_content(content[0]), format_content(content[1])]

def format_content(content):
    return [[c[:1], int(c[1:])] for c in content.split(',')]

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
