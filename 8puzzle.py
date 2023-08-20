import copy

def find_coordinates(grid, target):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == target:
                return (i, j)
            
def is_adjacent(pos1, pos2):
    # Check if two positions are adjacent
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2) == 1
            
def get_direction(from_pos, to_pos):
    # Determine the direction from one position to another
    x1, y1 = from_pos
    x2, y2 = to_pos

    if x1 < x2:
        return "down"
    elif x1 > x2:
        return "up"
    elif y1 < y2:
        return "right"
    elif y1 > y2:
        return "left"

def check_legal_moves(grid):
    legal_moves = []
    b_position = find_coordinates(grid, 'b')
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != 'b':
                if is_adjacent(b_position, (i, j)):
                    legal_moves.append(get_direction(b_position, (i, j)))
    
    return legal_moves

def calculate_h(start_grid, goal_grid):
    differences = 0
    for i in range(len(start_grid)):
        for j in range(len(start_grid[i])):
            if start_grid[i][j] != 'b':
                if start_grid[i][j] != goal_grid[i][j]:
                    differences += 1

    return differences

def swap_positions(grid, direction):
    swapped_grid = copy.deepcopy(grid)
    b_position = find_coordinates(swapped_grid, 'b')
    if direction == 'up':
        target_position = (b_position[0] - 1, b_position[1])
    elif direction == 'down':
        target_position = (b_position[0] + 1, b_position[1])
    elif direction == 'left':
        target_position = (b_position[0], b_position[1] - 1)
    elif direction == 'right':
        target_position = (b_position[0], b_position[1] + 1)

    xt, yt = target_position
    xb, yb = b_position
    swapped_grid[xt][yt], swapped_grid[xb][yb] = swapped_grid[xb][yb], swapped_grid[xt][yt]
    return {"grid": swapped_grid, "direction": direction}

def generate_successors(grid):
    successors = []
    legal_moves = check_legal_moves(grid)
    for move in legal_moves:
        successors.append(swap_positions(grid, move))
    return successors

def check_solved(start_grid, goal_grid):
    differences = 0
    for i in range(len(start_grid)):
        for j in range(len(start_grid[i])):
            if start_grid[i][j] != 'b':
                if start_grid[i][j] != goal_grid[i][j]:
                    differences += 1

    if differences == 0:
        return True
    else:
        return False

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    def put(self, priority, item):
        self.elements.append((priority, item))
        self.elements.sort(key=lambda x: x[0])

    def get(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.elements.pop(0)[1]

start = [['u','h','u'],['g','u','h'],['u','b','u']]
goal = [['h','u','b'],['u','u','u'],['h','u','g']]

closed = []

pq = PriorityQueue()
pq.put(0, {"grid": start, "g_cost": 0, "moves": "start"})

while not pq.is_empty():
    current_state = pq.get()
    closed.append(current_state["grid"])

    if check_solved(current_state["grid"], goal):
        print(current_state)
        break

    successors = generate_successors(current_state["grid"]) # [{"grid": swapped_grid, "direction": direction}, {"grid": swapped_grid, "direction": direction}]
    filtered_successors = []
    for successor in successors:
        if successor["grid"] not in closed:
            filtered_successors.append(successor)

    for successor in filtered_successors:
        g_cost = current_state["g_cost"] + 1
        h_cost = calculate_h(successor["grid"], goal)
        f_cost = g_cost + h_cost
        successor_state = {"grid": successor["grid"], "g_cost": g_cost, "moves": current_state["moves"] + ' ' + successor["direction"]}
        pq.put(f_cost, successor_state)
    
