from pygame import Vector2
from collections import deque
import heapq

class BFS():
    def __init__(self, snake, goal):
        self.snake = snake
        self.start = self.snake.snake[0]
        self.goal = goal

    def Solving(self):
        queue = deque([self.start])
        path = {tuple(self.start): None}

        while (queue):
            state = queue.popleft()
            if(state == self.goal):
                goal_path = deque()
                while state is not None:
                    goal_path.append(state)
                    state = path[tuple(state)]
                goal_path.reverse()
                return goal_path

            for substate in self.snake.Is_safe(state):
                if(tuple(substate) not in path):
                    queue.append(substate)
                    path[tuple(substate)] = state
        return None

class DFS():
    def __init__(self, snake, goal):
        self.snake = snake
        self.start = self.snake.snake[0]
        self.goal = goal

    def Solving(self):
        queue = deque([self.start])
        path = {tuple(self.start): None}

        while (queue):
            state = queue.pop()
            if(state == self.goal):
                goal_path = deque()
                while state is not None:
                    goal_path.append(state)
                    state = path[tuple(state)]
                goal_path.reverse()
                return goal_path

            for substate in self.snake.Is_safe(state):
                if(tuple(substate) not in path):
                    queue.append(substate)
                    path[tuple(substate)] = state
        return None

class UCS():
    def __init__(self, screen, tile_size, snake, goal):
        self.screen_width, self.screen_height = screen.get_size()
        self.screen_rows, self.screen_cols = self.screen_height // tile_size, self.screen_width // tile_size
        self.tile_size = tile_size
        self.snake = snake
        self.start = self.snake.snake[0]
        self.goal = goal

    def Solving(self):
        start_state = (int(self.start.x), int(self.start.y))
        queue = [(0, start_state)]
        path = {start_state: None}
        cost_path = {start_state: 0}
        while(queue):
            cost, state = heapq.heappop(queue)
            state_Vector2 = Vector2(*state)
            if(state_Vector2 == self.goal):
                goal_path = deque()
                while state is not None:
                    goal_path.append(Vector2(*state))
                    state = path[state]
                goal_path.reverse()
                return goal_path

            for substate_Vector2 in self.snake.Is_safe(state):
                substate = (int(substate_Vector2.x), int(substate_Vector2.y))
                if(substate not in path):
                    new_cost = self.Cost_calc(self.snake,substate_Vector2, cost)
                    if(tuple(substate) not in cost_path or new_cost < cost_path[tuple(substate)]):
                        cost_path[tuple(substate)] = new_cost
                        heapq.heappush(queue, (new_cost, substate))
                        path[tuple(substate)] = state

    def Cost_calc(self, snake, substate, cost):
        state = (int(substate.x), int(substate.y))
        if(state in snake.high_dangerzone):
            return cost + 3
        elif(state in snake.med_dangerzone):
            return cost + 2
        elif(state in snake.low_dangerzone):
            return cost + 1
        elif(state in snake.verylow_dangerzone):
            return cost

class Greedy():
    def __init__(self, snake, goal):
        self.snake = snake
        self.start = self.snake.snake[0]
        self.goal = goal
        self.penalty = 10000

    def Heuristic_calc(self, snake, head, tail, h_map, P):
        floodfill_h = h_map.get(head, P)
        tail_safe = self.Tail_heuristic(snake, head, tail)

        if(tail_safe): return floodfill_h
        else: return floodfill_h + P

    def Flood_fill(self, snake, goal, obstacles = None):
        distance_map = {tuple(goal): 0}
        queue = deque([tuple(goal)])
        if(obstacles is None):
            obstacles = {(w.x, w.y) for w in self.snake.wall_pos}
            obstacles.update((seg.x, seg.y) for seg in self.snake.snake)

        while(queue):
            state = queue.popleft()
            distance = distance_map[state]
            for d in snake.direction:
                next_x = state[0] + d.x
                next_y = state[1] + d.y
                next_state = (next_x, next_y)

                if(next_x < 0 or next_x >= self.snake.screen_cols or
                   next_y < 0 or next_y >= self.snake.screen_rows): continue
                if(next_state in obstacles): continue
                if next_state not in distance_map:
                    distance_map[next_state] = distance + 1
                    queue.append(next_state)
        return distance_map

    def Tail_heuristic(self, snake, head, tail):
        obstacles = {(w.x, w.y) for w in self.snake.wall_pos}
        obstacles.update((seg.x, seg.y) for seg in self.snake.snake[:-1])
        tail_map = self.Flood_fill(snake, tail, obstacles)
        return head in tail_map


    def Solving(self):
        flood_fill = self.Flood_fill(self.snake, (self.goal.x, self.goal.y))
        start_state = (int(self.start.x), int(self.start.y))
        tail_tuple = (self.snake.snake[-1].x, self.snake.snake[-1].y)
        initial_heuristic = self.Heuristic_calc(self.snake, start_state, tail_tuple, flood_fill, 100000)
        queue = [(initial_heuristic, start_state)]
        path = {start_state: None}
        while(queue):
            cost, state = heapq.heappop(queue)
            state_Vector2 = Vector2(*state)
            if(state_Vector2 == self.goal):
                goal_path = deque()
                while state is not None:
                    goal_path.append(Vector2(*state))
                    state = path[state]
                goal_path.reverse()
                return goal_path
            for substate_Vector2 in self.snake.Is_safe(state):
                substate = (int(substate_Vector2.x), int(substate_Vector2.y))
                if substate not in path:
                    heuristic = self.Heuristic_calc(self.snake, substate, tail_tuple, flood_fill, self.penalty)
                    heapq.heappush(queue, (heuristic, substate))
                    path[substate] = state



class Beam:
    def __init__(self):
        pass

class SIMULATED_ANEALING:
    def __init__(self):
        pass

class FORWARD_CHECKING:
    def __init__(self):
        pass

class AC_3:
    def __init__(self):
        pass
