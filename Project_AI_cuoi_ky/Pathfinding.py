import random
import numpy as np
from pygame import Vector2
from collections import deque
import heapq

class BFS():
    def __init__(self, snake, goal, start = None):
        self.snake = snake
        if(start == None): self.start = self.snake.snake[0]
        else: self.start = start
        self.goal = goal

    def Solving(self):
        queue = deque([self.start])
        path = {tuple(self.start): None}

        while(queue):
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
        self.penalty = 50

    def Heuristic_calc(self, snake, head, tail, h_map, P):
        floodfill_h = h_map.get(head, P)
        tail_safe = self.Tail_heuristic(snake, head, tail)
        reachable_area = self.Reachable_area_heuristic(snake, head, 0.002)

        if(tail_safe): return floodfill_h + reachable_area
        else: return floodfill_h + P + reachable_area

    def Flood_fill(self, snake, goal, obstacles=None, limit=None):
        distance_map = {tuple(goal): 0}
        queue = deque([tuple(goal)])
        if (obstacles is None):
            obstacles = {(w.x, w.y) for w in self.snake.wall_pos}
            obstacles.update((seg.x, seg.y) for seg in self.snake.snake)

        while (queue):
            state = queue.popleft()
            distance = distance_map[state]
            if (limit is not None and distance >= limit): continue
            for d in snake.direction:
                next_x = state[0] + d.x
                next_y = state[1] + d.y
                next_state = (next_x, next_y)

                if (next_x < 0 or next_x >= self.snake.screen_cols or
                        next_y < 0 or next_y >= self.snake.screen_rows): continue
                if (next_state in obstacles): continue
                if next_state not in distance_map:
                    distance_map[next_state] = distance + 1
                    queue.append(next_state)
        return distance_map

    def Tail_heuristic(self, snake, head, tail):
        obstacles = {(w.x, w.y) for w in self.snake.wall_pos}
        obstacles.update((seg.x, seg.y) for seg in self.snake.snake[:-1])
        tail_map = self.Flood_fill(snake, tail, obstacles)
        return head in tail_map

    def Reachable_area_heuristic(self, snake, head, weight):
        safe_heuristic_limit = 10
        reachable_area = len(self.Flood_fill(snake, head, limit=safe_heuristic_limit))
        return -reachable_area * weight

    def Solving(self):
        flood_fill = self.Flood_fill(self.snake, (self.goal.x, self.goal.y))
        start_state = (int(self.start.x), int(self.start.y))
        tail_tuple = (self.snake.snake[-1].x, self.snake.snake[-1].y)
        initial_heuristic = self.Heuristic_calc(self.snake, start_state, tail_tuple, flood_fill, 200)
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

class BEAM:
    def __init__(self, snake, goal, K):
        self.snake = snake
        self.start = self.snake.snake[0]
        self.goal = goal
        self.beam_width = K
        self.penalty = 50

    def Heuristic_calc(self, snake, head, tail, h_map, P):
        floodfill_h = h_map.get(head, P)
        tail_safe = self.Tail_heuristic(snake, head, tail)
        reachable_area = self.Reachable_area_heuristic(snake, head, 0.002)

        if(tail_safe): return floodfill_h + reachable_area
        else: return floodfill_h + P + reachable_area

    def Flood_fill(self, snake, goal, obstacles=None, limit=None):
        distance_map = {tuple(goal): 0}
        queue = deque([tuple(goal)])
        if (obstacles is None):
            obstacles = {(w.x, w.y) for w in self.snake.wall_pos}
            obstacles.update((seg.x, seg.y) for seg in self.snake.snake)

        while (queue):
            state = queue.popleft()
            distance = distance_map[state]
            if (limit is not None and distance >= limit): continue
            for d in snake.direction:
                next_x = state[0] + d.x
                next_y = state[1] + d.y
                next_state = (next_x, next_y)

                if (next_x < 0 or next_x >= self.snake.screen_cols or
                        next_y < 0 or next_y >= self.snake.screen_rows): continue
                if (next_state in obstacles): continue
                if next_state not in distance_map:
                    distance_map[next_state] = distance + 1
                    queue.append(next_state)
        return distance_map

    def Tail_heuristic(self, snake, head, tail):
        obstacles = {(w.x, w.y) for w in self.snake.wall_pos}
        obstacles.update((seg.x, seg.y) for seg in self.snake.snake[:-1])
        tail_map = self.Flood_fill(snake, tail, obstacles)
        return head in tail_map

    def Reachable_area_heuristic(self, snake, head, weight):
        safe_heuristic_limit = 10
        reachable_area = len(self.Flood_fill(snake, head, limit=safe_heuristic_limit))
        return -reachable_area * weight

    def Solving(self):
        flood_fill = self.Flood_fill(self.snake, (self.goal.x, self.goal.y))
        start_state = (int(self.start.x), int(self.start.y))
        tail_tuple = (self.snake.snake[-1].x, self.snake.snake[-1].y)
        initial_heuristic = self.Heuristic_calc(self.snake, start_state, tail_tuple, flood_fill, 200)
        queue = [(initial_heuristic, start_state)]
        path = {start_state: None}

        while(queue):
            selected_states = []
            heapq.heapify(queue)
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
                        selected_states.append((heuristic, substate))
                        path[substate] = state
            heapq.heapify(selected_states)
            next_queue = []
            for i in range(min(self.beam_width, len(selected_states))):
                next_queue.append(heapq.heappop(selected_states))
            queue = next_queue
        return None


class SIMULATED_ANEALING:
    def __init__(self, snake, goal, T, alpha):
        self.snake = snake
        self.start = self.snake.snake[0]
        self.goal = goal
        self.Max_temp = T
        self.alpha = alpha
        self.penalty = 50

    def Heuristic_calc(self, snake, head, tail, h_map, P):
        floodfill_h = h_map.get(head, P)
        tail_safe = self.Tail_heuristic(snake, head, tail)
        reachable_area = self.Reachable_area_heuristic(snake, head, 0.002)

        if (tail_safe): return floodfill_h + reachable_area
        else: return floodfill_h + P + reachable_area

    def Flood_fill(self, snake, goal, obstacles = None, limit = None):
        distance_map = {tuple(goal): 0}
        queue = deque([tuple(goal)])
        if (obstacles is None):
            obstacles = {(w.x, w.y) for w in self.snake.wall_pos}
            obstacles.update((seg.x, seg.y) for seg in self.snake.snake)

        while (queue):
            state = queue.popleft()
            distance = distance_map[state]
            if(limit is not None and distance >= limit): continue
            for d in snake.direction:
                next_x = state[0] + d.x
                next_y = state[1] + d.y
                next_state = (next_x, next_y)

                if (next_x < 0 or next_x >= self.snake.screen_cols or
                        next_y < 0 or next_y >= self.snake.screen_rows): continue
                if (next_state in obstacles): continue
                if next_state not in distance_map:
                    distance_map[next_state] = distance + 1
                    queue.append(next_state)
        return distance_map

    def Tail_heuristic(self, snake, head, tail):
        obstacles = {(w.x, w.y) for w in self.snake.wall_pos}
        obstacles.update((seg.x, seg.y) for seg in self.snake.snake[:-1])
        tail_map = self.Flood_fill(snake, tail, obstacles)
        return head in tail_map

    def Reachable_area_heuristic(self, snake, head, weight):
        safe_heuristic_limit = 10
        reachable_area = len(self.Flood_fill(snake, head, limit = safe_heuristic_limit))
        return -reachable_area * weight

    def Solving(self):
        flood_fill = self.Flood_fill(self.snake, (self.goal.x, self.goal.y))
        start_state = (int(self.start.x), int(self.start.y))
        tail_tuple = (self.snake.snake[-1].x, self.snake.snake[-1].y)
        initial_heuristic = self.Heuristic_calc(self.snake, start_state, tail_tuple, flood_fill, 200)
        best_state = start_state
        best_h = initial_heuristic
        T = self.Max_temp

        while(T > 1):
            next_possible_state = self.Next_state(self.snake, start_state)
            if not(next_possible_state): break
            next_state = random.choice(next_possible_state)
            next_h = self.Heuristic_calc(self.snake, next_state, tail_tuple, flood_fill, 200)
            delta = next_h - initial_heuristic
            if(delta <= 0):
                start_state = next_state
                initial_heuristic = next_h
            else:
                P = np.exp(-delta / T)
                if(P > random.random()):
                    start_state = next_state
                    initial_heuristic = next_h
            if(initial_heuristic > best_h):
                best_h = initial_heuristic
                best_state = next_state
            T *= self.alpha

        bfs = BFS(self.snake, self.goal, start = Vector2(*best_state))
        goal_path = bfs.Solving()
        return goal_path

    def Next_state(self, snake, state):
        next_pos = []
        obstacles = {(w.x, w.y) for w in self.snake.wall_pos}
        obstacles.update((seg.x, seg.y) for seg in self.snake.snake)
        for d in snake.direction:
            next_x = state[0] + d.x
            next_y = state[1] + d.y
            next_state = (next_x, next_y)

            if (next_x < 0 or next_x >= self.snake.screen_cols or
                    next_y < 0 or next_y >= self.snake.screen_rows): continue
            if (next_state in obstacles): continue
            next_pos.append(next_state)

        return next_pos

class FORWARD_CHECKING:
    def __init__(self):
        pass

class AC_3:
    def __init__(self):
        pass
