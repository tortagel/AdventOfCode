INPUT_FILE = "Day-13\input.txt"

class IntPC:

    def __init__(self, program):
        self.POSITION_MODE = 0
        self.IMMEDIATE_MODE = 1
        self.RELATIVE_MODE = 2
        self.program = program
        self.output = []
        self.inst_ptr = 0
        self.relative_base = 0

    def save_access(self, i):
        while i >= len(self.program):
            self.program.append(0)
        return self.program[i]

    def save_assign(self, i, value):
        while i >= len(self.program):
            self.program.append(0)
        self.program[i] = value

    def run(self, input_value = None):
        while True:
            finish, _ = self.compute_step(input_value)
            if finish:
                break
        return self.output

    def compute_step(self, input_value = None, break_on_first_input = False):
        out = []
        input_used = False
        while True:
            # parse optcode and mode
            a = [int(x) for x in str(self.program[self.inst_ptr])]
            while len(a) < 5:
                a.insert(0, 0)
            A, B, C, D, E = a
            opcode = 10 * D + E

            if opcode in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                param1 = self.save_access(self.inst_ptr + 1)
                if C == self.POSITION_MODE:
                    param1_val = self.save_access(param1)
                elif C == self.IMMEDIATE_MODE:
                    param1_val = param1
                elif C == self.RELATIVE_MODE:
                    param1_val = self.save_access(self.relative_base + param1)
                    #print("param1_val={}".format(param1_val))
                else:
                    raise ValueError(f"wrong mode (C): {C}")
            
            if opcode in [1, 2, 5, 6, 7, 8]:
                param2 = self.save_access(self.inst_ptr + 2)
                if B == self.POSITION_MODE:
                    param2_val = self.save_access(param2)
                elif B == self.IMMEDIATE_MODE:
                    param2_val = param2
                elif B == self.RELATIVE_MODE:
                    param2_val = self.save_access(self.relative_base + param2)
                else:
                    raise ValueError(f"wrong mode (B): {B}")
                
            if opcode in [1, 2, 7, 8]:
                param3 = self.save_access(self.inst_ptr + 3)
                if A == self.POSITION_MODE:
                    param3_val = self.save_access(param3)
                elif A == self.IMMEDIATE_MODE:
                    param3_val = param3
                elif A == self.RELATIVE_MODE:
                    param3_val = self.save_access(self.relative_base + param3)
                else:
                    raise ValueError(f"wrong mode (A): {A}")

            if opcode == 1:
                if A == self.POSITION_MODE:
                    i = param3
                elif A == self.RELATIVE_MODE:
                    i = self.relative_base + param3
                self.save_assign(i, param1_val + param2_val)
                self.inst_ptr += 4
            elif opcode == 2:
                if A == self.POSITION_MODE:
                    i = param3
                elif A == self.RELATIVE_MODE:
                    i = self.relative_base + param3
                self.save_assign(i, param1_val * param2_val)
                self.inst_ptr += 4
            elif opcode == 3:
                # input
                if break_on_first_input:
                    return False, out
                if input_used:
                    return False, out
                if C == self.POSITION_MODE:
                    i = param1
                elif C == self.RELATIVE_MODE:
                    i = self.relative_base + param1
                self.save_assign(i, input_value)
                self.inst_ptr += 2
                input_used = True
            elif opcode == 4:
                # output
                out.append(param1_val)
                self.output.append(param1_val)
                self.inst_ptr += 2
            elif opcode == 5:
                if param1_val != 0:
                    self.inst_ptr = param2_val
                else:
                    self.inst_ptr += 3
            elif opcode == 6:
                if param1_val == 0:
                    self.inst_ptr = param2_val
                else:
                    self.inst_ptr += 3
            elif opcode == 7:
                if param1_val < param2_val:
                    value = 1
                else:
                    value = 0
                if A == self.POSITION_MODE:
                    i = param3
                elif A == self.RELATIVE_MODE:
                    i = self.relative_base + param3
                self.save_assign(i, value)
                self.inst_ptr += 4
            elif opcode == 8:
                if param1_val == param2_val:
                    value = 1
                else:
                    value = 0
                if A == self.POSITION_MODE:
                    i = param3
                elif A == self.RELATIVE_MODE:
                    i = self.relative_base + param3
                self.save_assign(i, value)
                self.inst_ptr += 4
            elif opcode == 9:
                # adjusts the relative base
                self.relative_base += param1_val
                self.inst_ptr += 2
            elif opcode == 99:
                break
            else:
                raise ValueError(f"something went wrong (opcode = {opcode})")
        
        return True, out

def move(intPc, game, joystick):
    if joystick == None:
        finish, output = intPc.compute_step(break_on_first_input=True)
    else:
        finish, output = intPc.compute_step(joystick)
    print(f"output={output}")
    score = None
    for i in range(0, len(output), 3):
        x = output[i]
        y = output[i + 1]
        if x == -1 and y == 0:
            score = output[i + 2]
        else:
            id = output[i+2]
            game[y][x] = id
    
    print_game(game)
    print(f"score={score}\n")

    return score


def solve_part1(content):
    intPc = IntPC(content)
    output = intPc.run()
    tiles = []
    for i in range(0, len(output), 3):
        id = output[i+2]
        tiles.append(id)
    return tiles.count(2)

def print_game(game):
    for g in game:
        print(g)

def solve_part2(content):
    return None

def prepare_content(content):
    return [int(i) for i in content[0].split(",")]

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
