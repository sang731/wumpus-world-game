import random

class LevelGenerator:
    def __init__(self, n):
        self.n = n
        self.pits = set()
        self.wumpus = None
        self.gold = None
        self.generate()

    def all_cells(self):
        return [(x, y) for x in range(1, self.n+1) for y in range(1, self.n+1)]

    def adjacent(self, cell):
        x,y = cell
        adj = []
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny = x+dx, y+dy
            if 1 <= nx <= self.n and 1 <= ny <= self.n:
                adj.append((nx,ny))
        return adj

    def has_neighboring_pits_in_same_row(self, cell, pits):
        x, y = cell
        
        for pit in pits:
            pit_x, pit_y = pit
            if pit_y == y:  
                if abs(pit_x - x) == 1:
                    return True
        return False

    def has_pits_blocking_origin(self, pits):
        return (1, 2) in pits and (2, 1) in pits

    def generate(self):
        cells = self.all_cells()
        forbidden = {(1,1)}  # Player starts at (1,1)
        pit_count = max(0, self.n - 1)
        possible = [c for c in cells if c not in forbidden]
        random.shuffle(possible)
        self.pits = set()

        for c in possible:
            if len(self.pits) >= pit_count:
                break
            if not self.has_neighboring_pits_in_same_row(c, self.pits):
                temp_pits = self.pits | {c}
                if not self.has_pits_blocking_origin(temp_pits):
                    self.pits.add(c)

        if len(self.pits) < pit_count:
            remaining_possible = [c for c in possible if c not in self.pits]
            for c in remaining_possible:
                if len(self.pits) >= pit_count:
                    break
                temp_pits = self.pits | {c}
                if not self.has_pits_blocking_origin(temp_pits):
                    self.pits.add(c)

        if self.has_pits_blocking_origin(self.pits):
            if random.choice([True, False]):
                self.pits.discard((1, 2))
            else:
                self.pits.discard((2, 1))

        available = [c for c in cells if c not in self.pits and c != (1,1)]
        if not available:
            self.wumpus = (self.n, self.n)
        else:
            self.wumpus = random.choice(available)

        available = [c for c in cells if c not in self.pits and c != (1,1) and c != self.wumpus]
        random.shuffle(available)
        chosen = None
        tries = 0
        for c in available:
            adj = self.adjacent(c)
            blocked = sum(1 for a in adj if a in self.pits or a == self.wumpus)
            if blocked < len(adj):
                chosen = c
                break
            tries += 1
            if tries > 200:
                break

        if chosen is None:
            chosen = available[0] if available else (self.n, self.n)
        self.gold = chosen