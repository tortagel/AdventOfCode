from itertools import groupby

INPUT_FILE = "Day-4\input.txt"

def solve_part1(content):
    n1 = content[0]
    n2 = content[1]
    count = 0
    for n in range(n1, n2+1):
        a = [int(x) for x in str(n)]
        # from left to right, the digits never decrease
        if all(x <= y for x, y in zip(a, a[1:])):
            # two adjacent digits are the same
            if sum([ (len(list(group)) > 1 if 1 else 0)  for key, group in groupby(a)]) > 0:
                count += 1
    return count

def solve_part2(content):
    n1 = content[0]
    n2 = content[1]
    count = 0
    for n in range(n1, n2+1):
        a = [int(x) for x in str(n)]
        # from left to right, the digits never decrease
        if all(x <= y for x, y in zip(a, a[1:])):
            # the two adjacent matching digits are not part of a larger group of matching digits
            if sum([ (len(list(group)) == 2 if 1 else 0)  for key, group in groupby(a)]) > 0:
                count += 1
    return count

def prepare_content(content):
    return [int(n) for n in content[0].split('-')]

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
