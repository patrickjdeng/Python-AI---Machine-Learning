'''
Patrick Deng
Cs 4375.501

via read_states_from_file
First open file, read in each state's name and reward, then:
    create list of actions for each state, adding the state, and the corresponding transition to each
    action's transition list depending on action name of the transition. The final result is an interconnected
    series of actions from each state, and transitions from each action.


Then for 20 iterations:
Base iteration: Each state's policy has a random action, and the state would have a j-value of its own reward.
Successive iterations:
Each state's chosen policy has the best j-value, the policy chosen through find_best_policy() for each state.
Each policy has its own action and j-value, each
j-value calculated by reward +discount*SUM_ACROSS_ACTIONS_TRANSITIONS(probability of each transition given the action).
Then find_best_policy() returns the policy that yields the highest j-value, i.e. the source state, action, and j-value

Then we have generated a 20 row table of policies for each state.
We use print_policy_table to output for each iteration, each best policy for each state;
FORMAT: (source_state action_to_take resultant-j_value)

'''

import sys
import random
import decimal


class State:
    def __init__(self, name, reward):
        self.name = name
        self.reward = reward
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)


class Action:
    def __init__(self, source, name):
        self.source = source
        self.name = name
        self.transitions = []

    def add_transition(self, transition):
        self.transitions.append(transition)


class Transition:
    def __init__(self, source, target, prob):
        self.source = source
        self.target = target
        self.prob = prob


class Policy:
    def __init__(self, state, action, j_val):
        self.state = state
        self.action = action
        self.j_val = j_val


def main():
    states = read_states_from_file(sys.argv[1])
    discount = float(sys.argv[2])
    iteration_count = 20
    policy_table = []
    # fill up policy table
    for row_index in range(iteration_count):
        policy_row = []
        if row_index == 0:
            for state in states:
                action = state.actions[random.randint(0, len(state.actions)-1)]
                j_val = state.reward
                policy_row.append(Policy(state, action, j_val))
        else:
            for state in states:
                policy = find_best_policy(state, discount, policy_table[row_index - 1], states)
                policy_row.append(policy)
        policy_table.append(policy_row)
    print_policy_table(policy_table)


def index_of(name, array):
    for index in range(len(array)):
        if array[index].name == name:
            return index
    return -1


def read_states_from_file(filename):
    file = open(filename)
    state_list = []
    for row in file:
        # after split by '(': ['name REWARD','ACTION TARGET PROB)','TRANSITION)', ...]
        partitions = row.strip('\n').split(" (")
        source_name = partitions[0].split(' ')[0]
        source_reward = float(partitions[0].split(' ')[1])
        current_source = State(source_name, source_reward)
        state_list.append(current_source)
        for transition in partitions[1:]:
            transition = transition.strip(')').split(' ')
            action_name = transition[0]
            target_name = transition[1]
            prob = float(transition[2])
            if index_of(action_name, current_source.actions) == -1:
                current_source.add_action(Action(source_name, action_name))
            current_source.actions[index_of(action_name, current_source.actions)].\
                add_transition(Transition(source_name, target_name, prob))
    # replace all target state names with their actual states
    for state in state_list:
        for action in state.actions:
            for transition in action.transitions:
                transition.target = state_list[index_of(transition.target, state_list)]
    return state_list


def find_best_policy(source_state, discount_factor, past_policies, states_list):
    # TODO
    j_values = []
    # calculate j-values for each action
    for action in source_state.actions:
        current_j_val = source_state.reward
        for transition in action.transitions:
            target_j_val = past_policies[index_of(transition.target.name, states_list)].j_val
            current_j_val += discount_factor * transition.prob * target_j_val
        j_values.append(current_j_val)

    # find maximum j-val and its index
    best_action_index = 0
    for i in range(len(source_state.actions)):
        if j_values[i] > j_values[best_action_index]:
            best_action_index = i

    best_action = source_state.actions[best_action_index]
    return Policy(source_state, best_action, j_values[best_action_index])


def print_policy_table(policy_table):
    # print out iteration number, not index
    for index in range(0, len(policy_table)):
        row_string = "After iteration " + str(index + 1) + ": "
        for policy in policy_table[index]:
            FOURPLACES = decimal.Decimal(10)**-4
            policy_jval_string = str(decimal.Decimal(policy.j_val).quantize(FOURPLACES))
            row_string += " (" + policy.state.name + " " + policy.action.name + " " + policy_jval_string + ")"
        print(row_string)
    return


main()
