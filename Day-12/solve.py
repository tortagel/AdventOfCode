from itertools import combinations

INPUT_FILE = "Day-12\input.txt"

class Dim:

    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

class Moon:

    def __init__(self, pos_x, pos_y, pos_z, name = "Moon"):
        self.position = Dim(pos_x, pos_y, pos_z)
        self.velocity = Dim()
        self.name = name

    def __repr__(self):
        s = f"{self.name} {{ position=({self.position.x}, {self.position.y}, {self.position.z}),"
        s += f" velocity=({self.velocity.x}, {self.velocity.y}, {self.velocity.z}) }}"
        return s

    def __eq__(self, other):
        return self.position == other.position and self.velocity == other.velocity

    def move(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.position.z += self.velocity.z

    def apply_gravity(self, other_moon):
        if self.position.x < other_moon.position.x:
            self.velocity.x += 1
            other_moon.velocity.x -= 1
        elif self.position.x > other_moon.position.x:
            self.velocity.x -= 1
            other_moon.velocity.x += 1
        if self.position.y < other_moon.position.y:
            self.velocity.y += 1
            other_moon.velocity.y -= 1
        elif self.position.y > other_moon.position.y:
            self.velocity.y -= 1
            other_moon.velocity.y += 1
        if self.position.z < other_moon.position.z:
            self.velocity.z += 1
            other_moon.velocity.z -= 1
        elif self.position.z > other_moon.position.z:
            self.velocity.z -= 1
            other_moon.velocity.z += 1

    def get_potential_energy(self):
        return abs(self.position.x) + abs(self.position.y) + abs(self.position.z)

    def get_kinetic_energy(self):
        return abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)
    
    def get_total_energy(self):
        return self.get_potential_energy() * self.get_kinetic_energy()


def motion_step(moons):
    # 1. update velocity by applying gravity
    pairs = combinations(moons, 2)
    
    for (moon1, moon2) in pairs:
        moon1.apply_gravity(moon2)

    # 2. update position by applying velocity
    for moon in moons:
        moon.move()

def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return (a * b) // gcd(a, b)

def parse_moons(content):
    return [ Moon(moon[0], moon[1], moon[2], f"Moon{i}") for i, moon in enumerate(content) ]

def solve_part1(content):
    moons = parse_moons(content)
    for _ in range(1000):
        motion_step(moons)
    return sum([ moon.get_total_energy() for moon in moons ]) # total system energy

def solve_part2(content):
    moons = parse_moons(content)
    steps = [-1, -1, -1]
    for axe in range(3):
        step = 0
        seen = set()
        while True:
            motion_step(moons)
            a = []
            for moon in moons:
                if axe == 0:
                    a.append((moon.position.x, moon.velocity.x))
                elif axe == 1:
                    a.append((moon.position.y, moon.velocity.y))
                elif axe == 2:
                    a.append((moon.position.z, moon.velocity.z))
            a = str(a)
            if a in seen:
                steps[axe] = step
                break
            else:             
                step += 1   
                seen.add(a)
    return lcm(lcm(steps[0], steps[1]), steps[2])

def prepare_content(content):
    result = []
    for line in content:
        x = int(line[line.index('x=') + 2: line.index(', y')])
        y = int(line[line.index('y=') + 2: line.index(', z')])
        z = int(line[line.index('z=') + 2: line.index('>')])
        result.append((x, y, z))
    return result

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
