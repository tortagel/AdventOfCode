INPUT_FILE = "Day-1\input.txt"

def calc_fuel(n):
    return (n // 3) - 2

def calc_fuel_ex(n):
    l = []
    n = calc_fuel(n)
    while n > 0:
        l.append(n)
        n = calc_fuel(n)
    return sum(l)


def solve_part1(lines):
    result = [calc_fuel(n) for n in lines]
    return sum(result)

def solve_part2(lines):
    result = [calc_fuel_ex(n) for n in lines]
    return sum(result)

def handle_input(content):
    return [int(n) for n in content]

def solve_puzzle(part, filename):
    with open(filename, 'r') as file:
        content = file.readlines()
        content = [x.strip() for x in content]
        content = handle_input(content)
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
