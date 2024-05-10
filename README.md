# Multi Agent Pacman Capture the Flag - AI Algorithms

This repository contains the implementation and analysis of Monte Carlo Tree Search (MCTS) and Heuristic Algorithms within a multi-agent Pacman Capture the Flag environment. This project was developed as part of an assignment for the Modern Game AI Algorithms course at Leiden University in 2024.

## Project Overview
The project focuses on developing AI agents that can efficiently control both Pacman and ghost characters in a team-based strategy game setting. The game environment consists of two opposing teams aiming to collect food pellets from each other's side while defending against ghost attacks.

### Game Mechanics
- **Scoring:** Points are earned by collecting food pellets and returning them to the team's starting area.
- **Power Capsules:** When consumed, these capsules turn enemy ghosts into a "scared" state, making them vulnerable to being captured.
- **End Conditions:** The game ends when a team collects nearly all pellets from the opponent's side or when the move limit is reached.

## Algorithms Implemented
1. **Monte Carlo Tree Search (MCTS):**
   - MCTS is used to simulate various gameplay scenarios to make the most informed decision at each game state.
   - The algorithm explores possible actions by balancing between known good actions and exploring new actions to optimize the gameplay strategy.

2. **Heuristic Algorithm:**
   - Utilizes predefined heuristic rules to make decisions, which are faster but might not always lead to optimal solutions compared to MCTS.
   - Focuses on immediate payoffs and defensive strategies to safeguard against opposing team advances.

## Tournament
- Conducted a local tournament to compare the performance of MCTS and Heuristic algorithms.
- The tournament involved 30 games, measuring effectiveness based on the number of food pellets collected and overall win rates.

## Key Findings
- The Heuristic algorithm showed a higher win rate and was generally more efficient in decision-making.
- MCTS provided better performance in terms of depth of strategy and long-term decision-making.

## Future Work
- Combining MCTS with Deep Reinforcement Learning (DRL) to enhance decision-making capabilities.
- Implementing advanced node selection policies like UCB1-Tuned and Progressive Widening to improve the search process in MCTS.

## Python3 version of UC Berkeley's CS 188 Pacman Capture the Flag project

## Getting Started

### Command Line :

run `python capture.py`

capture.py is already modified with MCTS.py and Heuristic.py

running `python capture.py` will perform a tournament between these two agents.


### Environment:

The challenge is to design agents to play Capture-the-Flag in a Pacman-like
arena.   

![Example Game](/origdoc/capture_the_flag.png)

#### Rules

**Layout:** The Pacman map is divided into two halves: blue (right) and red (left).  Red agents (which all have even indices) must defend the red food while trying to eat the blue food.  When on the red side, a red agent is a ghost.  When crossing into enemy territory, the agent becomes a Pacman.

**Scoring:**  When a Pacman eats a food dot, the food is stored up inside of that Pacman and removed from the board.  When a Pacman returns to his side of the board, he "deposits" the food dots he is carrying, earning one point per food pellet delivered.  Red team scores are positive, while Blue team scores are negative.

**Eating Pacman:** When a Pacman is eaten by an opposing ghost, the Pacman returns to its starting position (as a ghost).  The food dots that the Pacman was carrying are deposited back onto the board.  No points are awarded for eating an opponent.

**Power capsules:** If Pacman eats a power capsule, agents on the opposing team become "scared" for the next 40 moves, or until they are eaten and respawn, whichever comes sooner.  Agents that are "scared" are susceptible while in the form of ghosts (i.e. while on their own team's side) to being eaten by Pacman.  Specifically, if Pacman collides with a "scared" ghost, Pacman is unaffected and the ghost respawns at its starting position (no longer in the "scared" state).

**Observations:** Agents can only observe an opponent's configuration (position and direction) if they or their teammate is within 5 squares (Manhattan distance).  In addition, an agent always gets a noisy distance reading for each agent on the board, which can be used to approximately locate unobserved opponents.

**Winning:** A game ends when one team eats all but two of the opponents' dots.  Games are also limited to 1200 agent moves (300 moves per each of the four agents).  If this move limit is reached, whichever team has eaten the most food wins. If the score is zero (i.e., tied) this is recorded as a tie game.

**Computation Time:** Each agent has 1 second to return each action. Each move which does not return within one second will incur a warning.  After three warnings, or any single move taking more than 3 seconds, the game is forfeit.  There will be an initial start-up allowance of 15 seconds (use the `registerInitialState` method). If you agent times out or otherwise throws an exception, an error message will be present in the log files, which you can download from the results page (see below).

#### Key data structures

`CaptureAgent` (in `captureAgent.py`) is a useful base class for your agents.
It has a variety of methods that can return useful information.  This includes a `distancer` field that contains a `distanceCalculator` object that can automatically calculate (and cache) the distances between every two points in the maze.

`GameState` (in `capture.py`) has still more information that can be queried.  A current `GameState` object is passed into your agents' `chooseAction` methods.  Note that `GameState` objects can return the set of legal actions for an agent and can generate new `GameState` s that would result from any action.

`game.py` has code that defines `Directions`, `Configurations`, `AgentState`, and a `Grid`, all of which might be handy and save extra work on your part.

`util.py` has code that might prove helpful.  Of particular note is the `Counter` class which implements a dictionary, but where unused keys default to mapping to 0 (instead of undefined).  A `Counter` mapping positions (integer pairs) to a real value can be used with `CaptureAgent.displayDistributionsOverPositions` to color the cells on the map with debugging information.

`myTeam.py` has skeleton code for generating a team of agents.  Its format should not be changed and needs to have the function `createTeam` as specified.  You should copy this file, change its name, and use it to build your own team.
