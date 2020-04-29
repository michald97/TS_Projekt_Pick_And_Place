from statemachine import StateMachine, State, Transition

# define states for a master (way of passing args to class)
line_1_options = [
    {"name": "IDLE_LINE_1", "initial": True, "value": "q0"},  # 0
    {"name": "MOVING_PACKAGE", "initial": False, "value": "q1"},  # 1
    {"name": "START_LINE1", "initial": False, "value": "q2"},  # 2
    {"name": "SENSOR", "initial": False, "value": "q3"},  # 3
    {"name": "END_PROCESS", "initial": False, "value": "q4"},  # 4
    {"name": "ERROR", "initial": False, "value": "q5"},  # 5
    {"name": "WAITING_FOR_RESTART", "initial": False, "value": "q6"}]  # 6


# create State objects for a master
# ** -> unpack dict to args
line_1_states = [State(**opt) for opt in line_1_options]


# valid transitions for a master (indices of states from-to)
line_1_form_to = [
    [0, [0, 1]],
    [1, [2, 5]],
    [2, [3, 5]],
    [3, [5, 4]],
    [5, [5, 6]],
    [6, [6, 1]],
    [4, [5, 0]]
]

# create transitions for a packing (as a dict)
line_1_transitions = {}
for indices in line_1_form_to:
    from_idx, to_idx_tuple = indices  # unpack list of two elements into separate from_idx and to_idx_tuple
    for to_idx in to_idx_tuple:  # iterate over destinations from a source state
        op_identifier = "l_{}_{}".format(from_idx, to_idx)  # parametrize identifier of a transition

        # create transition object and add it to the master_transitions dict
        transition = Transition(line_1_states[from_idx], line_1_states[to_idx], identifier=op_identifier)
        line_1_transitions[op_identifier] = transition

        # add transition to source state
        line_1_states[from_idx].transitions.append(transition)