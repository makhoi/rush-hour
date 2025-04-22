import random
from heapq import heappush, heappop
import util

class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost  # g(n)
        self.depth = 0 if parent is None else parent.depth + 1

    def path(self):
        """Return list of states from root to this node."""
        node, result = self, []
        while node:
            result.append(node.state)
            node = node.parent
        return list(reversed(result))

    def __lt__(self, other):
        """For priority queue sorting (based on cost or f-value)."""
        return self.cost < other.cost

class Agent:
    def __init__(self):
        pass

    def random_walk(self, state, n):
        """Performs a random walk of N steps starting from the given state."""
        current = Node(state)
        visited = [current.state]

        for _ in range(n):
            actions = current.state.actions()
            if not actions:
                break  # dead end, no more moves
            action = random.choice(actions)
            next_state = current.state.execute(action)
            current = Node(next_state, parent=current, action=action, cost=current.cost + 1)
            visited.append(current.state)

        return visited

    def bfs(self, state):
        """Breadth-First Search."""
        return self._search(state, strategy='bfs')

    def dfs(self, state):
        """Depth-First Search."""
        return self._search(state, strategy='dfs')

    def a_star(self, state, heuristic):
        """A* Search using provided heuristic function."""
        return self._search(state, strategy='a_star', heuristic=heuristic)
    
    def _search(self, state, strategy='bfs', heuristic=None):
        start = Node(state)
        if strategy == 'a_star' and heuristic:
            f = start.cost + heuristic(start.state)
            open_list = [(f, start)]
        else:
            open_list = [start]

        closed = set()

        while open_list:
            # BFS: pop first | DFS: pop last | A*: pop cheapest
            if strategy == 'bfs':
                node = open_list.pop(0)
            elif strategy == 'dfs':
                node = open_list.pop()
            elif strategy == 'a_star':
                node = heappop(open_list)[1]
            else:
                raise ValueError(f"Unknown strategy: {strategy}")

            util.pprint(node.path())  # print path to this node

            if node.state.is_goal():
                return node

            closed.add(str(node.state))

            for action in node.state.actions():
                new_state = node.state.execute(action)
                if str(new_state) not in closed:
                    cost = node.cost + 1
                    new_node = Node(new_state, parent=node, action=action, cost=cost)
                    if strategy == 'a_star' and heuristic:
                        f = cost + heuristic(new_state)
                        heappush(open_list, (f, new_node))  # A* stores tuple (f, node)
                    else:
                        open_list.append(new_node)

        return None  # No solution found