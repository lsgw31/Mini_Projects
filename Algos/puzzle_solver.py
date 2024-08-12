class Puzzle:
    def __init__(self, matrix_str: str):
        matrix_str += '0'  # represents empty square; from now on will view as the square moving rather than an empty space
        self.m = [[int(i) for i in matrix_str[:3]], [int(i) for i in matrix_str[3:6]], [int(i) for i in matrix_str[6:]]]
        self.moves = []

    def move0(self, direction: tuple[int], zero: tuple[int]):  # Base code to make a single slide
        to_coord = (zero[0] + direction[0], zero[1] + direction[1])
        self.m[zero[0]][zero[1]] = self.m[to_coord[0]][to_coord[1]]
        self.m[to_coord[0]][to_coord[1]] = 0
        self.moves.append(self.m[zero[0]][zero[1]])
    
    def solve(self) -> str:  # Chain all placex() methods together for modularity
        ret = '\nIf you entered your numbers correctly, this is what your puzzle should look like:\n'
        ret += '\033[1m' + '\n'.join(' '.join(str(j) if j else ' ' for j in i) for i in self.m) + '\033[0m'

        self.place1()
        ret += '\n'.join(self.yield_moves_and_puzzle())

        self.place23()
        ret += '\n'.join(self.yield_moves_and_puzzle())

        self.place47()
        ret += '\n'.join(self.yield_moves_and_puzzle())

        self.finish_solve()
        ret += '\n'.join(self.yield_moves_and_puzzle(solved = True))

        return ret
    
    def yield_moves_and_puzzle(self, *, solved: bool = False):
        yield '\n\n\nNow move tiles in this order:'
        yield ', '.join(str(i) for i in self.moves)
        self.moves.clear()
        if not solved:
            yield '\nYour puzzle should now look like this:'
            yield '\033[1m' + '\n'.join(' '.join(str(j) if j else ' ' for j in i) for i in self.m) + '\033[0m'
        else:
            yield'\n\033[1mYour puzzle should now be solved!\033[0m'
    
    def rotate2x2(self, coord: tuple[int], direction: str):  # rotate 0 around in clockwise/counterclockwise (c/cc) direction in a certain 2x2 quadrant provided by coord
        for i in range(4):
            self.move0(ALL_2X2_ROTATIONS[coord][len(direction) - 1][i], LOCATIONS_IN_ROTATIONS[coord][::-2 * len(direction) + 3][i])
    
    def place1(self):
        if self.m[2][1] == 1:  # put 0 in center; avoid putting 1 farther away than it already was from top left
            self.move0((-1, 0), (2, 2))
            self.move0((0, -1), (1, 2))
        elif self.m[1][1] == 1:
            self.move0((0, -1), (2, 2))
            self.move0((0, -1), (2, 1))
            self.move0((-1, 0), (2, 0))
            self.move0((0, 1), (1, 0))
        else:
            self.move0((0, -1), (2, 2))
            self.move0((-1, 0), (2, 1))
        
        direction = 'c' * ((1 in (self.m[1][0], self.m[2][0], self.m[2][1])) + 1)
        
        for numcoord, subcoord in ONE_ROTATIONS[direction]:
            if self.m[numcoord[0]][numcoord[1]] == 1:
                self.rotate2x2(subcoord, direction)
    
    def place23(self):
        if self.m[0][2] == 3 and self.m[0][1] != 2:
            if self.m[1][2] == 2:
                self.rotate2x2((1, 1), 'cc')
            self.rotate2x2((0, 1), 'c')
        elif self.m[0][1] == 2:
            self.rotate2x2((0, 1), 'cc')
        
        for numcoord, subcoord in TWO_AND_THREE_ROTATIONS:
            if self.m[numcoord[0]][numcoord[1]] == 2:
                self.rotate2x2(subcoord, 'c')
        
        for numcoord, subcoord in TWO_AND_THREE_ROTATIONS:
            if self.m[numcoord[0]][numcoord[1]] == 3:
                self.rotate2x2(subcoord, 'c')
    
    def place47(self):
        if self.m[2][0] == 7 and self.m[1][0] != 4:
            if self.m[2][1] == 4:
                self.rotate2x2((1, 1), 'cc')
            self.rotate2x2((1, 0), 'cc')
        
        for numcoord, subcoord in FOUR_AND_SEVEN_ROTATIONS:
            if self.m[numcoord[0]][numcoord[1]] == 4:
                self.rotate2x2(subcoord, 'cc')
        
        for numcoord, subcoord in FOUR_AND_SEVEN_ROTATIONS:
            if self.m[numcoord[0]][numcoord[1]] == 7:
                self.rotate2x2(subcoord, 'cc')
    
    def finish_solve(self):
        self.moves.extend(FINAL_ROTATIONS[tuple(self.m[1][2:] + self.m[2][1:])])


ALL_2X2_ROTATIONS = {
    (0, 0): (((0, -1), (-1, 0), (0, 1), (1, 0)), 
             ((-1, 0), (0, -1), (1, 0), (0, 1))),

    (0, 1): (((-1, 0), (0, 1), (1, 0), (0, -1)), 
             ((0, 1), (-1, 0), (0, -1), (1, 0))),

    (1, 0): (((1, 0), (0, -1), (-1, 0), (0, 1)), 
             ((0, -1), (1, 0), (0, 1), (-1, 0))),

    (1, 1): (((0, 1), (1, 0), (0, -1), (-1, 0)), 
             ((1, 0), (0, 1), (-1, 0), (0, -1)))
}

LOCATIONS_IN_ROTATIONS = {
    (0, 0): ((1, 1), (1, 0), (0, 0), (0, 1), (1, 1)), 
    
    (0, 1): ((1, 1), (0, 1), (0, 2), (1, 2), (1, 1)), 
    
    (1, 0): ((1, 1), (2, 1), (2, 0), (1, 0), (1, 1)), 
    
    (1, 1): ((1, 1), (1, 2), (2, 2), (2, 1), (1, 1))
}


ONE_ROTATIONS = {
    'c': (
        ((1, 2), (0, 1)), 
        ((0, 2), (0, 1)), 
        ((0, 1), (0, 0))
        ),

    'cc': (
        ((2, 1), (1, 0)), 
        ((2, 0), (1, 0)), 
        ((1, 0), (0, 0))
        )
}

TWO_AND_THREE_ROTATIONS = (
    ((1, 0), (1, 0)),
    ((2, 0), (1, 0)),
    ((2, 1), (1, 1)),
    ((2, 2), (1, 1)),
    ((1, 2), (0, 1))
)

FOUR_AND_SEVEN_ROTATIONS = (
    ((1, 0), (1, 0)),
    ((1, 2), (1, 1)),
    ((2, 2), (1, 1)),
    ((2, 1), (1, 0))
)

FINAL_ROTATIONS = {
    (6, 5, 8): [5, 8],
    (5, 8, 6): [5, 6],
    (8, 6, 5): [6, 5, 8, 6, 5, 8],
}

if __name__ == '__main__':
    print(Puzzle(input('\033[1mEnter the numbers in the order that they appear on the grid: \033[0m')).solve())
