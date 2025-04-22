import sys
from rushhour import State, DEFAULT_STATE
from agent import Agent
import util

def blocking_heuristic(state):
    board = str(state).split('|')
    exit_row = board[2]  # row where 'x' is always located
    index = exit_row.find('x') + 2  # position just after the red car
    blockers = 0
    for i in range(index, 6):
        if exit_row[i] != ' ':
            blockers += 1
    return blockers

def main():
    cmd = util.get_arg(1)
    board_string = util.get_arg(2)
    state = State(board_string) if board_string else State(DEFAULT_STATE)

    agent = Agent()

    if cmd == "random":
        result = agent.random_walk(state, 8)
        util.pprint(result)

    elif cmd == "bfs":
        result = agent.bfs(state)
        if result:
            util.pprint(result.path())
        else:
            print("No solution found.")

    elif cmd == "dfs":
        result = agent.dfs(state)
        if result:
            util.pprint(result.path())
        else:
            print("No solution found.")

    elif cmd == "a_star":
        result = agent.a_star(state, blocking_heuristic)
        if result:
            util.pprint(result.path())
        else:
            print("No solution found.")

if __name__ == "__main__":
    main()

