from statemachine import StateMachine, State, Transition

# define states for a master (way of passing args to class)
options = [
    {"name": "IDLE", "initial": True, "value": "idle"},  # 0
    {"name": "PACKING", "initial": False, "value": "packing"},  # 1
    {"name": "PICK_AND_PLACE_1", "initial": False, "value": "line_1"},  # 2
    {"name": "PICK_AND_PLACE_2", "initial": False, "value": "line_2"},  # 3
    {"name": "WRAPPER", "initial": False, "value": "wrapper"},  # 4
    {"name": "STOP", "initial": False, "value": "stop"},  # 5
    {"name": "ERROR_MESSAGE", "initial": False, "value": "error"}]  # 6


# create State objects for a master
# ** -> unpack dict to args
master_states = [State(**opt) for opt in options]


# valid transitions for a master (indices of states from-to)
form_to = [
    [0, [0, 1]],
    [1, [2, 6]],
    [2, [3, 6]],
    [3, [4, 6]],
    [4, [5, 6]],
    [6, [6, 5]],
    [5, [5, 0]]
]


# create transitions for a master (as a dict)
master_transitions = {}
for indices in form_to:
    from_idx, to_idx_tuple = indices  # unpack list of two elements into separate from_idx and to_idx_tuple
    for to_idx in to_idx_tuple:  # iterate over destinations from a source state
        op_identifier = "m_{}_{}".format(from_idx, to_idx)  # parametrize identifier of a transition

        # create transition object and add it to the master_transitions dict
        transition = Transition(master_states[from_idx], master_states[to_idx], identifier=op_identifier)
        master_transitions[op_identifier] = transition

        # add transition to source state
        master_states[from_idx].transitions.append(transition)