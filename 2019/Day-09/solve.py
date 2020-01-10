INPUT_FILE = "Day-9\input.txt"
POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2

def save_access(program, i):
    while i >= len(program):
        program.append(0)
    return program[i]

def save_assign(program, i, value):
    while i >= len(program):
        program.append(0)
    program[i] = value

def compute(program, input_value):
    output = []
    inst_ptr = 0
    relative_base = 0
    while True:
        # parse optcode and mode
        a = [int(x) for x in str(program[inst_ptr])]
        while len(a) < 5:
            a.insert(0, 0)
        A, B, C, D, E = a
        opcode = 10 * D + E

        param1 = save_access(program, inst_ptr + 1)
        if C == POSITION_MODE:
            param1_val = save_access(program, param1)
        elif C == IMMEDIATE_MODE:
            param1_val = param1
        elif C == RELATIVE_MODE:
            param1_val = save_access(program, relative_base + param1)
        else:
            print("wrong mode (C): {}".format(C))
            break
        
        param2 = save_access(program, inst_ptr + 2)
        if B == POSITION_MODE:
            param2_val = save_access(program, param2)
        elif B == IMMEDIATE_MODE:
            param2_val = param2
        elif B == RELATIVE_MODE:
            param2_val = save_access(program, relative_base + param2)
        else:
            print("wrong mode (B): {}".format(C))
            break
            
        param3 = save_access(program, inst_ptr + 3)
        if A == POSITION_MODE:
            param3_val = save_access(program, param3)
        elif A == IMMEDIATE_MODE:
            param3_val = param3
        elif A == RELATIVE_MODE:
            param3_val = save_access(program, relative_base + param3)
        else:
            print("wrong mode (A): {}".format(C))
            break

        if opcode == 1:
            if A == POSITION_MODE:
                i = param3
            elif A == RELATIVE_MODE:
                i = relative_base + param3
            save_assign(program, i, param1_val + param2_val)
            inst_ptr += 4
        elif opcode == 2:
            if A == POSITION_MODE:
                i = param3
            elif A == RELATIVE_MODE:
                i = relative_base + param3
            save_assign(program, i, param1_val * param2_val)
            inst_ptr += 4
        elif opcode == 3:
            # input
            print("input")
            if C == POSITION_MODE:
                i = param1
            elif C == RELATIVE_MODE:
                i = relative_base + param1
            save_assign(program, i, input_value)
            inst_ptr += 2
        elif opcode == 4:
            # output
            output.append(param1_val)
            inst_ptr += 2
        elif opcode == 5:
            if param1_val != 0:
                inst_ptr = param2_val
            else:
                inst_ptr += 3
        elif opcode == 6:
            if param1_val == 0:
                inst_ptr = param2_val
            else:
                inst_ptr += 3
        elif opcode == 7:
            if param1_val < param2_val:
                value = 1
            else:
                value = 0
            if A == POSITION_MODE:
                i = param3
            elif A == RELATIVE_MODE:
                i = relative_base + param3
            save_assign(program, i, value)
            inst_ptr += 4
        elif opcode == 8:
            if param1_val == param2_val:
                value = 1
            else:
                value = 0
            if A == POSITION_MODE:
                i = param3
            elif A == RELATIVE_MODE:
                i = relative_base + param3
            save_assign(program, i, value)
            inst_ptr += 4
        elif opcode == 9:
            # adjusts the relative base
            relative_base += param1_val
            inst_ptr += 2
        elif opcode == 99:
            break
        else:
            print("something went wrong (opcode = {})".format(opcode))
            break

    return output

def solve_part1(content):
    return compute(content, 1)

def solve_part2(content):
    return compute(content, 2)

def prepare_content(content):
    return [int(inst_ptr) for inst_ptr in content[0].split(",")]

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
