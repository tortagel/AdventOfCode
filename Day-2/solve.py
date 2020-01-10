INPUT_FILE = "Day-2\input.txt"

def compute(program, noun, verb):
    program[1] = noun
    program[2] = verb
    for n in range(0, len(program), 4):
        opcode = program[n]
        if opcode == 1:
            program[program[n+3]] = program[program[n+1]] + program[program[n+2]]
        elif opcode == 2:
            program[program[n+3]] = program[program[n+1]] * program[program[n+2]]
        elif opcode == 99:
            break
        else:
            print("something went wrong")
            break

    return program[0]

def solve_part1(content):
    return compute(content, 12, 2)

def solve_part2(content):
    for noun in range(0, 100):
        for verb in range(0, 100):
            if compute(content.copy(), noun, verb) == 19690720:
                return 100 * noun + verb
    return None
    

def prepare_content(content):
    return [int(n) for n in content[0].split(",")]

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
