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
        if (obstacles is None): obstacles.update((seg.x, seg.y) for seg in self.snake.snake)

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
        obstacles = snake.wall_pos_set
        obstacles.update((seg.x, seg.y) for seg in self.snake.snake[:-1])
        tail_map = self.Flood_fill(snake, tail, obstacles)
        return head in tail_map

    def Reachable_area_heuristic(self, snake, head, weight):
        safe_heuristic_limit = 10
        reachable_area = len(self.Flood_fill(snake, head, limit=safe_heuristic_limit))
        return -reachable_area * weight

    def Solving(self):
        flood_fill = self.Flood_fill(self.snake, (self.goal.x, self.goal.y), self.snake.wall_pos_set)
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
        if(obstacles is None): obstacles.update((seg.x, seg.y) for seg in self.snake.snake)

        while(queue):
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
        obstacles = snake.wall_pos_set
        obstacles.update((seg.x, seg.y) for seg in self.snake.snake[:-1])
        tail_map = self.Flood_fill(snake, tail, obstacles)
        return head in tail_map

    def Reachable_area_heuristic(self, snake, head, weight):
        safe_heuristic_limit = 10
        reachable_area = len(self.Flood_fill(snake, head, limit=safe_heuristic_limit))
        return -reachable_area * weight

    def Solving(self):
        flood_fill = self.Flood_fill(self.snake, (self.goal.x, self.goal.y), self.snake.wall_pos_set)
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
        if(obstacles is None): obstacles.update((seg.x, seg.y) for seg in self.snake.snake)

        while(queue):
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
        obstacles = snake.wall_pos_set
        obstacles.update((seg.x, seg.y) for seg in self.snake.snake[:-1])
        tail_map = self.Flood_fill(snake, tail, obstacles)
        return head in tail_map

    def Reachable_area_heuristic(self, snake, head, weight):
        safe_heuristic_limit = 10
        reachable_area = len(self.Flood_fill(snake, head, limit = safe_heuristic_limit))
        return -reachable_area * weight

    def Solving(self):
        flood_fill = self.Flood_fill(self.snake, (self.goal.x, self.goal.y), self.snake.wall_pos_set)
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
        obstacles = snake.wall_pos_set
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

class SENSORLESS:
    def __init__(self, snake, goal, grid_size):
        self.snake = snake
        self.goal = goal
        self.grid_size = grid_size

    def Initial_belief_state(self):
        safe_cells = set()
        obstacles = self.snake.wall_pos_set
        obstacles.update((seg.x, seg.y) for seg in self.snake.snake)

        for x in range(self.snake.screen_cols):
            for y in range(self.snake.screen_rows):
                cell = (x, y)
                if cell not in obstacles:
                    safe_cells.add(cell)
        return safe_cells

    def Belief_heuristic(self, belief_set, flood_fill):
        if not belief_set:
            return float('inf')
        total_ff_cost = 0
        for state in belief_set:
            total_ff_cost += flood_fill.get(state, self.grid_size)

        avg_ff_cost = total_ff_cost / len(belief_set)
        uncertainty_penalty = len(belief_set)
        return (uncertainty_penalty * self.grid_size) + avg_ff_cost

    def Simulate_snake_move(self, snake_list, action_vector):
        if not snake_list: return []
        current_head_pos = snake_list[0]
        new_head_pos = current_head_pos + action_vector
        new_snake_list = [new_head_pos] + snake_list[:-1]

        return new_snake_list

    def Apply_move_belief(self, current_belief, action_vector, current_snake_body):
        next_belief = set()
        next_snake_body = self.Simulate_snake_move(current_snake_body, action_vector)
        obstacles = self.snake.wall_pos_set.copy()
        obstacles.update((s.x, s.y) for s in next_snake_body[1:])

        for pos_tuple in current_belief:
            pos_vec = Vector2(pos_tuple[0], pos_tuple[1])
            next_pos_vec = pos_vec + action_vector
            next_pos_tuple = (int(next_pos_vec.x), int(next_pos_vec.y))

            if (0 <= next_pos_vec.x < self.snake.screen_cols and
                    0 <= next_pos_vec.y < self.snake.screen_rows and
                    next_pos_tuple not in obstacles):
                next_belief.add(next_pos_tuple)

        return next_belief, next_snake_body

    def Solving(self):
        initial_belief = self.Initial_belief_state()
        initial_body = self.snake.snake
        goal_pos = (self.goal.x, self.goal.y)
        greedy = Greedy(self.snake, self.goal)
        flood_fill = greedy.Flood_fill(self.snake, goal_pos, self.snake.wall_pos_set)

        initial_h = self.Belief_heuristic(initial_belief, flood_fill)
        queue = [(initial_h, frozenset(initial_belief), None, None, initial_body)]
        path_tracking = {frozenset(initial_belief): (None, None, initial_body)}

        while queue:
            h_cost, current_frozenset, _, _, current_snake_body = heapq.heappop(queue)
            current_belief = set(current_frozenset)

            if current_belief == {goal_pos}: return self._reconstruct_action_path(path_tracking, current_frozenset)

            for d in self.snake.direction:
                next_belief, next_snake_body = self.Apply_move_belief(current_belief, d, current_snake_body)

                if not next_belief: continue
                next_frozenset = frozenset(next_belief)

                if next_frozenset not in path_tracking:
                    next_h = self.Belief_heuristic(next_belief, flood_fill)
                    heapq.heappush(queue, (next_h, next_frozenset, current_frozenset, d, next_snake_body))
                    path_tracking[next_frozenset] = (current_frozenset, d, current_snake_body)

        return None  # No path of Belief States found

    def _reconstruct_action_path(self, path_tracking, final_frozenset):
        action_path = deque()
        current_frozenset = final_frozenset

        while path_tracking.get(current_frozenset) and path_tracking[current_frozenset][0] is not None:
            parent_frozenset, action_vector, _ = path_tracking[current_frozenset]
            action_path.appendleft(action_vector)
            current_frozenset = parent_frozenset

        return action_path


class PARTIALLY_OBSERVABLE:
    def __init__(self, snake, goal, grid_size):
        self.snake = snake
        self.goal = goal
        self.grid_size = grid_size
        self.penalty = 50
        self.rad = 5

    def Initial_belief_state(self, obstacles):
        safe_cells = set()

        for x in range(self.snake.screen_cols):
            for y in range(self.snake.screen_rows):
                cell = (x, y)
                if cell not in obstacles:
                    safe_cells.add(cell)
        return safe_cells

    def Observable(self, head):
        visible = set()
        x_start = max(0, int(head.x) - self.rad)
        x_end = min(self.snake.screen_cols, int(head.x) + self.rad + 1)
        y_start = max(0, int(head.y) - self.rad)
        y_end = min(self.snake.screen_rows, int(head.y) + self.rad + 1)

        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                visible.add((x, y))
        return visible

    def Heuristic_calc(self, goal, next_tile, flood_fill, visible, Penalty = None):
        Penalty = self.penalty if Penalty is None else Penalty
        h_unknown = 0
        if(goal in visible): h_goal = flood_fill.get(next_tile, self.grid_size)
        else: h_goal = self.grid_size * 2

        is_on_boundery = any((next_tile[0] + d.x, next_tile[1] + d.y) not in visible for d in self.snake.direction)
        if(is_on_boundery): h_unknown += Penalty * h_goal
        return h_unknown + h_goal

    def Solving(self):
        initial_head = (int(self.snake.snake[0].x), int(self.snake.snake[0].y))
        goal_pos = (self.goal.x, self.goal.y)
        greedy = Greedy(self.snake, self.goal)
        flood_fill = greedy.Flood_fill(self.snake, goal_pos, self.snake.wall_pos_set)
        initial_h = self.Heuristic_calc(goal_pos, initial_head, flood_fill, self.Observable(Vector2(initial_head[0], initial_head[1])))

        obstacles = self.snake.wall_pos_set
        obstacles.update((seg.x, seg.y) for seg in self.snake.snake)

        queue = [(initial_h, initial_head )]
        path = {initial_head: None}
        while(queue):
            h, state = heapq.heappop(queue)
            stateVector2 = Vector2(state[0], state[1])
            if (stateVector2 == self.goal):
                goal_path = deque()
                while state is not None:
                    goal_path.append(state)
                    state = path[state]
                goal_path.reverse()
                solution = deque(Vector2(goal[0], goal[1]) for goal in goal_path)
                return solution

            visible = self.Observable(stateVector2)
            for substate_Vector2 in self.snake.Is_safe(stateVector2):
                substate = (int(substate_Vector2.x), int(substate_Vector2.y))
                if substate not in path:
                    heuristic = self.Heuristic_calc(goal_pos, substate, flood_fill, visible)
                    heapq.heappush(queue, (heuristic, substate))
                    path[substate] = state


class FORWARD_CHECKING:
    def __init__(self):
        pass

class AC_3:
    def __init__(self):
        pass
