from itertools import permutations

INPUT_FILE = "Day-7\input.txt"

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

    def compute_step(self, input_value = None):
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

def test_setting_ex(intPc, input_signal, phase_setting = None):
    if phase_setting != None:
        _, _ = intPc.compute_step(phase_setting)
    finish, output_signal = intPc.compute_step(input_signal)
    return finish, output_signal[0]

def test_setting(program, phase_setting, input_signal):
    intPc = IntPC(program.copy())
    _, _ = intPc.compute_step(phase_setting)
    _, output_signal = intPc.compute_step(input_signal)
    return output_signal[0]

def solve_part1(content):
    in_signal_A = 0
    thruster_signals = []
    for A, B, C, D, E in permutations(range(5)):
        in_signal_B = test_setting(content, A, in_signal_A)
        in_signal_C = test_setting(content, B, in_signal_B)
        in_signal_D = test_setting(content, C, in_signal_C)
        in_signal_E = test_setting(content, D, in_signal_D)
        out_signal = test_setting(content, E, in_signal_E)
        thruster_signals.append(out_signal)
    return max(thruster_signals)

def solve_part2(content):
    thruster_signals = []
    for A, B, C, D, E in permutations(range(5, 10)):
        amplifier_A = IntPC(content.copy())
        amplifier_B = IntPC(content.copy())
        amplifier_C = IntPC(content.copy())
        amplifier_D = IntPC(content.copy())
        amplifier_E = IntPC(content.copy())
        _, in_signal_B = test_setting_ex(amplifier_A, 0, A)
        _, in_signal_C = test_setting_ex(amplifier_B, in_signal_B, B)
        _, in_signal_D = test_setting_ex(amplifier_C, in_signal_C, C)
        _, in_signal_E = test_setting_ex(amplifier_D, in_signal_D, D)
        finish, out_signal = test_setting_ex(amplifier_E, in_signal_E, E)
        while not finish:
            _, in_signal_B = test_setting_ex(amplifier_A, out_signal)
            _, in_signal_C = test_setting_ex(amplifier_B, in_signal_B)
            _, in_signal_D = test_setting_ex(amplifier_C, in_signal_C)
            _, in_signal_E = test_setting_ex(amplifier_D, in_signal_D)
            finish, out_signal = test_setting_ex(amplifier_E, in_signal_E)
        thruster_signals.append(out_signal)        
    return max(thruster_signals)

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
