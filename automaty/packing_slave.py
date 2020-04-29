from statemachine import StateMachine, State, Transition

# define states for a master (way of passing args to class)
packing_options = [
    {"name": "IDLE_PACKING", "initial": True, "value": "p0"},  # 0
    {"name": "P1", "initial": False, "value": "p1"},  # 1
    {"name": "P2", "initial": False, "value": "p2"},  # 2
    {"name": "P3", "initial": False, "value": "p3"},  # 3
    {"name": "P4", "initial": False, "value": "p4"},  # 4
    {"name": "P5", "initial": False, "value": "p5"},  # 5
    {"name": "P6", "initial": False, "value": "p6"},  # 6
    {"name": "P7", "initial": False, "value": "p7"}]  # 6


# create State objects for a master
# ** -> unpack dict to args
packing_states = [State(**opt) for opt in packing_options]


# valid transitions for a master (indices of states from-to)
packing_form_to = [
    [0, [0, 1]],
    [1, [2, 6]],
    [2, [3, 6]],
    [3, [4, 6]],
    [4, [5, 6]],
    [6, [6, 7]],
    [7, [7, 1]],
    [5, [5, 0]]
]

# create transitions for a packing (as a dict)
packing_transitions = {}
for indices in packing_form_to:
    from_idx, to_idx_tuple = indices  # unpack list of two elements into separate from_idx and to_idx_tuple
    for to_idx in to_idx_tuple:  # iterate over destinations from a source state
        op_identifier = "p_{}_{}".format(from_idx, to_idx)  # parametrize identifier of a transition

        # create transition object and add it to the master_transitions dict
        transition = Transition(packing_states[from_idx], packing_states[to_idx], identifier=op_identifier)
        packing_transitions[op_identifier] = transition

        # add transition to source state
        packing_states[from_idx].transitions.append(transition)
