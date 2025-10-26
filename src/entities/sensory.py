def has_breeze(player_pos, pits, n):
    x,y = player_pos
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        nx,ny = x+dx, y+dy
        if 1 <= nx <= n and 1 <= ny <= n and (nx,ny) in pits:
            return True
    return False

def has_shine(player_pos, gold_pos, n):
    x,y = player_pos
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        nx,ny = x+dx, y+dy
        if 1 <= nx <= n and 1 <= ny <= n and (nx,ny) == gold_pos:
            return True
    return False

def has_stench(player_pos, wumpus_pos, wumpus_alive, n):
    if not wumpus_alive:
        return False
    x,y = player_pos
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        nx,ny = x+dx, y+dy
        if 1 <= nx <= n and 1 <= ny <= n and (nx,ny) == wumpus_pos:
            return True
    return False