from random import random

class Inf(list):
    def __getitem__(self, index: int):
        if 0 <= index < len(self): 
            return super().__getitem__(index)
        else:
            return {int: 0, Inf: Inf([0])}[type(self[0])]


class GameOfLife:
    def __init__(self, size: int = 50, chance: float = 0.25):
        self.size = size
        self.m = Inf([Inf([int(random() < chance) for i in range(size)]) for j in range(size)])
    
    def find_next_state(self):
        for row in range(self.size):
            for cell in range(self.size):
                if not self.m[row][cell]:  # 0: 0 -> 0 | 1: 1 -> 1 | 2: 0 -> 1 | 3: 1 -> 0
                    self.m[row][cell] = int(self.find_num_living_neighbors((row, cell)) == 3) * 2
                else:
                    self.m[row][cell] = (1 - int(self.find_num_living_neighbors((row, cell)) in (2, 3))) * 2 + 1
        
        for row in range(self.size):
            for cell in range(self.size):
                self.m[row][cell] = int(self.m[row][cell] in (1, 2))

    def find_num_living_neighbors(self, coord: tuple):
        return sum(map(
                       lambda i: self.m[i[0] + coord[0]][i[1] + coord[1]] % 2, 
                       ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
                       ))
