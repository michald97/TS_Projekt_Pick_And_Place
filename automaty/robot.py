from statemachine import StateMachine, State, Transition

# define states for a master (way of passing args to class)
packing_options = [
    {"name": "IDLE_ROBOT", "initial": True, "value": "q0"},  # 0
    {"name": "START_ROBOT", "initial": False, "value": "q1"},  # 1
    {"name": "MOVE_TO_OBJECT", "initial": False, "value": "q2"},  # 2
    {"name": "SUCKER", "initial": False, "value": "q3"},  # 3
    {"name": "MOVE_OBJECT", "initial": False, "value": "q4"},  # 4
    {"name": "SUCKER_OFF", "initial": False, "value": "q5"},  # 5
    {"name": "END_ROBOT", "initial": False, "value": "q6"},  # 6
    {"name": "ERROR", "initial": False, "value": "q7"},  # 7
    {"name": "WAITING_FOR_RESTART", "initial": False, "value": "q8"}]  # 8


# create State objects for a master
# ** -> unpack dict to args
robot_states = [State(**opt) for opt in packing_options]


# valid transitions for a master (indices of states from-to)
robot_form_to = [
    [0, [0, 1]],
    [1, [2, 7]],
    [2, [3, 7]],
    [3, [4, 7]],
    [4, [5, 7]],
    [5, [6, 7]],
    [7, [7, 8]],
    [8, [8, 1]],
    [6, [0]]
]

# create transitions for a packing (as a dict)
robot_transitions = {}
for indices in robot_form_to:
    from_idx, to_idx_tuple = indices  # unpack list of two elements into separate from_idx and to_idx_tuple
    for to_idx in to_idx_tuple:  # iterate over destinations from a source state
        op_identifier = "r_{}_{}".format(from_idx, to_idx)  # parametrize identifier of a transition

        # create transition object and add it to the master_transitions dict
        transition = Transition(robot_states[from_idx], robot_states[to_idx], identifier=op_identifier)
        robot_transitions[op_identifier] = transition

        # add transition to source state
        robot_states[from_idx].transitions.append(transition)