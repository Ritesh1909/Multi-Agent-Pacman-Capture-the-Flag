
import random, time, util
from captureAgents import CaptureAgent
from game import Directions


def createTeam(firstIndex, secondIndex, isRed, first='PacmanAgent', second='GhostAgent'):
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

# MCTS Algorithm Class
class MCTS_Algorithm(object):

    def __init__(self, gameState, agent, action, parent, ghost_position, center_line):

        self.node_visted = 1
        self.Qvalue = 0.0
        self.child = []
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0
        self.parent_node = parent
        self.ghost_position = ghost_position
        self.action = action
        self.gameState = gameState.deepCopy()

        all_actions = gameState.getLegalActions(agent.index)
        self.available_action = []
        for action in all_actions:
            if action != 'Stop':
                self.available_action.append(action)

        self.actions_not_explored = list(self.available_action)
        self.center_line = center_line

        self.agent = agent
        self.rewards = 0
        self.epsilon_value = 0.9

    # Mcts function 
    def mcts(self):
        max_iterations = 5000
        start_time = time.time()
        for i in range(max_iterations):
            if time.time() - start_time >= 0.98:
                break
            node_selected = self.expand_node()
            reward = node_selected.calculate_reward()
            node_selected.mcts_backpropagation(reward)
            best_child_selected = self.select_best_child().action
        return best_child_selected

    # Node expanded
    def expand_node(self):
        if self.depth >= 15:
            return self

        if self.actions_not_explored:
            current_game_state = self.gameState.deepCopy()
            action = self.actions_not_explored[-1]
            self.actions_not_explored = self.actions_not_explored[:-1]
            next_game_state = current_game_state.generateSuccessor(self.agent.index, action)
            new_node = MCTS_Algorithm(next_game_state, self.agent, action, self, self.ghost_position, self.center_line)
            self.child.append(new_node)
            return new_node

        if random.random() < self.epsilon_value:
            new_best_next_node = self.select_best_child()
        else:
            new_best_next_node = random.choice(self.child)
        return new_best_next_node.expand_node()

    # Select child
    def select_best_child(self):
        select_child = None
        highest_score = -99999
        for select in self.child:
            child_score = (select.Qvalue / select.node_visted)
            if child_score > highest_score:
                highest_score = child_score
                select_child = select
        return select_child

    # Calculare Reward 
    def calculate_reward(self):
        agent_current_position = self.gameState.getAgentPosition(self.agent.index)
        if agent_current_position == self.gameState.getInitialAgentPosition(self.agent.index):
            return -1000
        feature = util.Counter()
        agent_current_position = self.gameState.getAgentPosition(self.agent.index)
        distances_to_border = []
        for center_position in self.center_line:
            distance = self.agent.getMazeDistance(agent_current_position, center_position)
            distances_to_border.append(distance)
        minimum_distance = min(distances_to_border)
        feature['min_distance'] = minimum_distance
        feature_value = feature['min_distance']
        weight = {'min_distance': -1}
        weight_value = weight['min_distance']
        value = feature_value * weight_value
        return value

    def mcts_backpropagation(self, reward):
        self.Qvalue += reward
        self.node_visted += 1
        if self.parent_node is not None:
            self.parent_node.mcts_backpropagation(reward)


##########
# Agents #
##########

# Pacman Agesnt Class 
class PacmanAgent(CaptureAgent):

    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)
        # Height of the map
        self.map_height = gameState.data.layout.height
        # Width of the map
        self.map_width = gameState.data.layout.width
        self.map_divider = self.my_team_centerline(gameState)

    # Choose Pacman Action
    def chooseAction(self, gameState):

        agent_state = gameState.getAgentState(self.index)
        Pacman_agent = agent_state.isPacman
        actions = gameState.getLegalActions(self.index)
        food_eaten = agent_state.numCarrying

        if Pacman_agent:

            ghost_near_agent_position = []
            for ghost in self.check_enemy_ghost_threat(gameState):
                ghost_near_agent_position.append(gameState.getAgentPosition(ghost))

            available_food = self.getFood(gameState).asList()
            
            for opponent in self.getOpponents(gameState):
                ghost_state = gameState.getAgentState(opponent)
                scared_time = ghost_state.scaredTimer
                if scared_time > 10:
                    action_values = []
                    for action in actions:
                        action_values.append(self.feature_calculation(gameState, action))
                    heighest_action_value = max(action_values)
                    best_available_actions = []
                    for action, value in zip(actions, action_values):
                        if value == heighest_action_value:
                            best_available_actions.append(action)
                    selected_action = random.choice(best_available_actions)
                    return selected_action

            available_food_length = len(available_food)

            if not ghost_near_agent_position and food_eaten <= 4:

                action_values = []
                for action in actions:
                    action_values.append(self.feature_calculation(gameState, action))
                heighest_action_value = max(action_values)

                best_available_actions = []
                for action, value in zip(actions, action_values):
                    if value == heighest_action_value:
                        best_available_actions.append(action)
                selected_action = random.choice(best_available_actions)
                return selected_action


            elif available_food_length < 2 or food_eaten > 7:
                initialize_mcts = MCTS_Algorithm(gameState, self, None, None, ghost_near_agent_position,
                                                 self.map_divider)
                selected_action = MCTS_Algorithm.mcts(initialize_mcts)
                return selected_action
            else:
                initialize_mcts = MCTS_Algorithm(gameState, self, None, None, ghost_near_agent_position,
                                                 self.map_divider)
                selected_action = MCTS_Algorithm.mcts(initialize_mcts)
                return selected_action
            
        else:
            return GhostAgent.chooseAction(self, gameState)

    
    # Next State
    def get_next_state(self, gameState, action):

        return gameState.generateSuccessor(self.index, action)

    # Check for enemy gost in range
    def check_enemy_ghost_threat(self, gameState):

        ghosts = self.check_enemy_ghost(gameState)
        my_agent_position = gameState.getAgentPosition(self.index)
        EnemyGhosts_Threat = []

        for ghost in ghosts:
            ghost_distance = self.getMazeDistance(my_agent_position, gameState.getAgentPosition(ghost))
            if ghost_distance <= 3:
                EnemyGhosts_Threat.append(ghost)

        return EnemyGhosts_Threat

    # Calculate agent's minimum distance to food
    def check_min_dist_to_food(self, gameState):
        my_agent_position = gameState.getAgentPosition(self.index)
        food_positions = self.getFood(gameState).asList()

        food_distances = []
        for food in food_positions:
            distance_to_food = self.getMazeDistance(my_agent_position, food)
            food_distances.append(distance_to_food)

        shortest_distance_to_food = min(food_distances)

        return shortest_distance_to_food

    # Calculate Centerline
    def my_team_centerline(self, gameState):

        redTeam = self.red
        center_walls = gameState.getWalls().asList()
        if redTeam:
            center_x = ((self.map_width // 2) - 1)
        else:
            center_x = (self.map_width // 2)

        center_line = []

        for height in range(self.map_height):
            point_on_center = (center_x, height)

            center_line.append(point_on_center)

        center_positions = []
        for x, y in center_line:

            if (x, y) not in center_walls and (x + 1 - 2 * self.red, y) not in center_walls:
                center_positions.append((x, y))

        return center_positions

    # Defensive feature
    def defensive_features(self, gameState, action):

        defensive_features = util.Counter()
        successor = self.get_next_state(gameState, action)
        available_food = self.getFood(successor).asList()
        defensive_features['successorScore'] = -len(available_food)

        if len(available_food) > 0:
            current_pos = successor.getAgentState(self.index).getPosition()
            min_distance = min([self.getMazeDistance(current_pos, food) for food in available_food])
            defensive_features['distanceToFood'] = min_distance
        return defensive_features

    # Calculate feature
    def feature_calculation(self, gameState, action):

        next_game_state = self.get_next_state(gameState, action)
        next_state_food = next_game_state.getAgentState(self.index).numCarrying
        food_eaten = gameState.getAgentState(self.index).numCarrying
        features_counter = util.Counter()

        if next_state_food > food_eaten:
            features_counter['getFood'] = 1
        else:
            if len(self.getFood(next_game_state).asList()) > 0:
                features_counter['minDistToFood'] = self.check_min_dist_to_food(next_game_state)
        features = features_counter

        weights = {'minDistToFood': -1, 'getFood': 100}
        return features * weights

    #  Return defensive weights
    def defensive_weights(self, gameState, action): # maybe can change this as well

        defensive_weights = {'successorScore': 100, 'distanceToFood': -1}
        return defensive_weights

    # Evaluate defensive action
    def defensive_action_evaluate(self, gameState, action):

        features_value = self.defensive_features(gameState, action) # so this is getting both defensive_feature values
        weights_value = self.defensive_weights(gameState, action)
        return features_value * weights_value

    # Check for enemy ghost
    def check_enemy_ghost(self, gameState):

        EnemyGhostList = []
        for enemy_ghost in self.getOpponents(gameState):
            enemyGostState = gameState.getAgentState(enemy_ghost)

            if (enemyGostState.scaredTimer == 0) and (not enemyGostState.isPacman):
                enemyGostState_position = gameState.getAgentPosition(enemy_ghost)
                if enemyGostState_position != None:
                    EnemyGhostList.append(enemy_ghost)

        return EnemyGhostList


# Ghost agent class
class GhostAgent(CaptureAgent):

    # Initialize state
    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)

    # Choose Action for Ghost agent
    def chooseAction(self, gameState):
        agent_state = gameState.getAgentState(self.index)
        Pacman_agent = agent_state.isPacman

        if not Pacman_agent:
            actions = gameState.getLegalActions(self.index)
            selected_action = random.choice(actions)
            action_values = []
            for action in actions:
                value = self.defensive_action_evaluate(gameState, action)
                action_values.append(value)
            heighest_action_value = max(action_values)
            best_available_actions = []
            for action, value in zip(actions, action_values):
                if value == heighest_action_value:
                    best_available_actions.append(action)
            selected_action = random.choice(best_available_actions)
        return selected_action
    
    # Evaluate defensive action
    def defensive_action_evaluate(self, gameState, action):
        features_value = self.defensive_features(gameState, action)
        weights_value = self.defensive_weights(gameState, action)
        return features_value * weights_value

    # Return defensive features
    def defensive_features(self, gameState, action):
        next_game_state = self.get_next_state(gameState, action)
        agent_state = next_game_state.getAgentState(self.index)

        agent_position = agent_state.getPosition()
        defensive_features = util.Counter()

        if not agent_state.isPacman:
            defensive_features['defensive'] = 1
        else:
            defensive_features['defensive'] = 0

        Opponent_list = []

        for n in self.getOpponents(next_game_state):
            opponent_state = next_game_state.getAgentState(n)
            Opponent_list.append(opponent_state)

        Opponent_pacman = []
        for opponent in Opponent_list:
            if opponent.isPacman and opponent.getPosition() is not None:
                Opponent_pacman.append(opponent)

        defensive_features['total_opponent_pacman'] = len(Opponent_pacman)

        if len(Opponent_pacman) > 0:
            Opponent_pacman_disctance = []
            for op in Opponent_pacman:
                Opponent_pacman_disctance.append(self.getMazeDistance(agent_position, op.getPosition()))
            defensive_features['op_distance'] = min(Opponent_pacman_disctance)

        if Directions.STOP == action:
            defensive_features['stop'] = 1
        back_directions = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if back_directions == action:
            defensive_features['back'] = 1

        return defensive_features

    # Return defensive weights
    def defensive_weights(self, gameState, action):
        return {'total_opponent_pacman': -1000, 'defensive': 100, 'op_distance': -10, 'stop': -100, 'back': -2}
    
    # Next state
    def get_next_state(self, gameState, action):
        return gameState.generateSuccessor(self.index, action)