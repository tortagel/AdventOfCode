INPUT_FILE = "Day-5\input.txt"
POSITION_MODE = 0
IMMEDIATE_MODE = 1

def compute1(program, input_val):    
    output = []
    n = 0
    while n < len(program):
        a = [int(x) for x in str(program[n])]
        while len(a) < 5:
            a.insert(0, 0)
        A, B, C, D, E = a
        opcode = 10 * D + E
        if opcode in [1, 2]:
            if C == POSITION_MODE:
                n1 = program[program[n+1]]
            elif C == IMMEDIATE_MODE:
                n1 = program[n+1]
            else:
                print("wrong mode (C): {}".format(C))
                break
        
            if B == POSITION_MODE:
                n2 = program[program[n+2]]
            elif B == IMMEDIATE_MODE:
                n2 = program[n+2]
            else:
                print("wrong mode (B): {}".format(C))
                break

            if A == POSITION_MODE:
                idx = program[n+3]
            else:
                print("wrong mode (A): {}".format(C))
                break

            if opcode == 1:
                program[idx] = n1 + n2
            if opcode == 2:
                program[idx] = n1 * n2

            n += 4
        elif opcode == 3:
            program[program[n+1]] = input_val
            n += 2
        elif opcode == 4:
            out = program[program[n+1]]
            output.append(out)
            n += 2
        elif opcode == 99:
            break
        else:
            print("something went wrong (opcode = {})".format(opcode))
            break

    if (sum(output[:-1]) != 0):
        print("output with errors: {}".format(output))
    
    return output[-1]

def compute2(program, input_val):
    output = []
    n = 0
    while n < len(program):
        a = [int(x) for x in str(program[n])]
        while len(a) < 5:
            a.insert(0, 0)
        A, B, C, D, E = a
        opcode = 10 * D + E

        if opcode in [1, 2, 5, 6, 7, 8]:

            if C == POSITION_MODE:
                n1 = program[program[n+1]]
            elif C == IMMEDIATE_MODE:
                n1 = program[n+1]
            else:
                print("wrong mode (C): {}".format(C))
                break
        
            if B == POSITION_MODE:
                n2 = program[program[n+2]]
            elif B == IMMEDIATE_MODE:
                n2 = program[n+2]
            else:
                print("wrong mode (B): {}".format(C))
                break
            
            if opcode in [1, 2, 7, 8]:
                if A == POSITION_MODE:
                    idx = program[n+3]
                else:
                    print("wrong mode (A): {}".format(C))
                    break

            if opcode == 1:
                program[idx] = n1 + n2
                n += 4
            elif opcode == 2:
                program[idx] = n1 * n2
                n += 4
            if opcode == 5:
                if n1 != 0:
                    n = n2
                else:
                    n += 3
            elif opcode == 6:
                if n1 == 0:
                    n = n2
                else:
                    n += 3
            elif opcode == 7:
                if n1 < n2:
                    program[idx] = 1
                else:
                    program[idx] = 0
                n += 4
            elif opcode == 8:
                if n1 == n2:
                    program[idx] = 1
                else:
                    program[idx] = 0
                n += 4

        elif opcode == 3:
            program[program[n+1]] = input_val
            n += 2
        elif opcode == 4:
            out = program[program[n+1]]
            output.append(out)
            n += 2
        elif opcode == 99:
            break
        else:
            print("something went wrong (opcode = {})".format(opcode))
            break

    if (len(output) != 1):
        print("output with errors: {}".format(output))
    
    return output[0]

def solve_part1(content):
    return compute1(content, 1)

def solve_part2(content):
    return compute2(content, 5)

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
    print("part 1: {}".format(result))

    result = solve_puzzle(2, INPUT_FILE)
    print("part 2: {}".format(result))

if __name__ == '__main__':
	main()
