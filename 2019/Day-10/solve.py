from math import tan, atan2, atan, degrees

INPUT_FILE = "Day-10\input.txt"

def can_see(ast_map, x1, x2, y1, y2):    
    diff_x = x1 - x2
    diff_y = y1 - y2
    tan_alpha = None
    if diff_x == 0:
        nx = 0
        ny = 1
        if y2 < y1:
            ny *= -1
    elif diff_y == 0:
        nx = 1
        ny = 0
        if x2 < x1:
            nx *= -1
    else:
        tan_alpha = diff_x / diff_y
    x3 = x1
    y3 = y1
    while True:
        if tan_alpha != None:
            if x2 > x1:
                x3 += 1    
            else:
                x3 -= 1
            a = x3 - x1
            b = a / tan_alpha
            if not b.is_integer():
                continue
            y3 = y1 + int(b)
        else:
            x3 += nx
            y3 += ny
        if x2 >= x1 and x3 >= x2 and y2 >= y1 and y3 >= y2:
            break
        if x2 <= x1 and x3 <= x2 and y2 <= y1 and y3 <= y2:
            break
        if x2 <= x1 and x3 <= x2 and y2 >= y1 and y3 >= y2:
            break
        if x2 >= x1 and x3 >= x2 and y2 <= y1 and y3 <= y2:
            break
        if ast_map[y3][x3] == '#':
            return False
    return True

def detected_asteroids(ast_map, x1, y1):
    count = 0
    for y2, l in enumerate(ast_map):
        for x2, a in enumerate(l):
            if (x1 != x2 or y1 != y2) and a == '#':
                if can_see(ast_map, x1, x2, y1, y2):
                    count += 1
    return count

def find_best(ast_map):
    max_count = 0
    pos_x = -1
    pos_y = -1
    for y, l in enumerate(ast_map):
        for x, a in enumerate(l):
            if a == '#':
                count = detected_asteroids(ast_map, x, y)
                if count > max_count:
                    max_count = count
                    pos_x = x
                    pos_y = y
    return max_count, pos_x, pos_y

def vaporize_all(ast_map, ast_calced, angels, x_best, y_best):
    counter = 0
    idx_angels = angels.index(90.0)
    while sum([a.count('#') for a in ast_map]) > 0:
        angel = angels[idx_angels]

        idx = [i for i, e in enumerate(ast_calced) if e[0] == angel][0]
        x_vaporized = -1
        y_vaporized = -1
        for (x, y) in ast_calced[idx][1]:
            if can_see(ast_map, x_best, x, y_best, y):

                x_vaporized = x
                y_vaporized = y
                counter += 1
                
                ast_map[y][x] = str(counter)
                break
        
        if x_vaporized != -1 and y_vaporized != -1:
            ast_calced[idx][1].remove((x_vaporized, y_vaporized))
        idx_angels = (idx_angels - 1) % len(angels)

def solve_part1(content):
    count, _, _ = find_best(content)
    return count

def solve_part2(content):
    _, x_best, y_best = find_best(content)

    content[y_best][x_best] = 'X'

    ast_calced = []
    angels = []

    for y, l in enumerate(content):
        for x, a in enumerate(l):
            if a == '#':
                # save angel, coord,
                if x_best - x == 0:
                    if y > y_best:
                        angel = 270.0
                    else:
                        angel = 90.0
                elif y_best - y == 0:
                    if x > x_best:
                        angel = 0.0
                    else:
                        angel = 180.0
                else:
                    angel = degrees( atan2(y_best - y ,   x - x_best) ) % 360
                if angels.count(angel) == 0:
                    angels.append(angel)
                idx = [i for i, e in enumerate(ast_calced) if e[0] == angel]
                if len(idx) > 0:
                    ast_calced[idx[0]][1].append((x, y))
                else:
                    ast_calced.append([angel, [(x, y)]])

    angels.sort()
    
    vaporize_all(content, ast_calced, angels, x_best, y_best)
    
    elem = '200'
    for i, l in enumerate(content):
        if elem in l:
            y_200 = i
            x_200 = l.index(elem)
            break

    return x_200 * 100 + y_200

def prepare_content(content):
    return [[c for c in s] for s in content]

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
