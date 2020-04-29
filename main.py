from automaty.packing_slave import *
from automaty.line_1 import *
from automaty.line_2 import *
from automaty.robot import *

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


# create a generator class
class Generator(StateMachine):
    states = []
    transitions = []
    states_map = {}
    current_state = None

    def __init__(self, states, transitions):

        # creating each new object needs clearing its variables (otherwise they're duplicated)
        self.states = []
        self.transitions = []
        self.states_map = {}
        self.current_state = states[0]

        # create fields of states and transitions using setattr()
        # create lists of states and transitions
        # create states map - needed by StateMachine to map states and its values
        for s in states:
            setattr(self, str(s.name).lower(), s)
            self.states.append(s)
            self.states_map[s.value] = str(s.name)

        for key in transitions:
            setattr(self, str(transitions[key].identifier).lower(), transitions[key])
            self.transitions.append(transitions[key])

        # super() - allows us to use methods of StateMachine in our Generator object
        super(Generator, self).__init__()

    # define a printable introduction of a class
    def __repr__(self):
        return "{}(model={!r}, state_field={!r}, current_state={!r})".format(
            type(self).__name__, self.model, self.state_field,
            self.current_state.identifier,
        )

    # method of creating objects in a flexible way (we can define multiple functions
    # which will create objects in different ways)
    @classmethod
    def create_master(cls, states, transitions) -> 'Generator':
        return cls(states, transitions)


# create paths from transitions (exemplary)
path_1 = ["m_0_1", "m_1_2", "m_2_3", "m_3_4", "m_4_5", "m_5_0"]
path_2 = ["m_0_1", "m_1_2", "m_2_3", "m_3_4", "m_4_6", "m_6_5", "m_5_0"]
path_3 = ["m_0_1", "m_1_2", "m_2_3", "m_3_6", "m_6_5", "m_5_0"]
path_4 = ["m_0_1", "m_1_2", "m_2_6", "m_6_5", "m_5_0"]
path_5 = ["m_0_1", "m_1_6", "m_6_5", "m_5_0"]
paths = [path_1, path_2, path_3,path_4,path_5]

packing_path = ["p_0_1", "p_1_2", "p_2_3", "p_3_6", "p_6_6", "p_6_7", "p_7_1", "p_1_2", "p_2_3","p_3_4","p_4_5","p_5_0"]
robot_path = ["r_0_1", "r_1_2", "r_2_3", "r_3_4", "r_4_5", "r_5_6"]
line_path = ["l_0_1", "l_1_2", "l_2_3", "l_3_4"]



# execute paths
for path in paths:

    # create a supervisor
    supervisor = Generator.create_master(master_states, master_transitions)
    print('\n' + str(supervisor))

    # run supervisor for exemplary path
    print("Executing path: {}".format(path))
    for event in path:

        # launch a transition in our supervisor
        master_transitions[event]._run(supervisor)
        print(supervisor.current_state)

        # add slave
        if supervisor.current_state.value == "packing":
            # TODO: automata 1 (for) slave1
            packing = Generator.create_master(packing_states, packing_transitions)
            #print('\n' + str(packing))
            print("Executing path: {}".format(packing_path))
            for packing_event in packing_path:
                packing_transitions[packing_event]._run(packing)
                print(packing.current_state)
                if(packing.current_state.value) == "p1":
                    robot = Generator.create_master(robot_states, robot_transitions)
                    print("Executing path: {}".format(robot_path))
                    for robot_event in robot_path:
                        robot_transitions[robot_event]._run(robot)
                        print(robot.current_state)
                if (packing.current_state.value) == "p3":
                    robot = Generator.create_master(robot_states, robot_transitions)
                    print("Executing path: {}".format(robot_path))
                    for robot_event in robot_path:
                        robot_transitions[robot_event]._run(robot)
                        print(robot.current_state)

        if supervisor.current_state.value == "line_1":
            # TODO: automata 2 (for) slave2
            line_1 = Generator.create_master(line_1_states, line_1_transitions)
            # print('\n' + str(packing))
            print("Executing path: {}".format(line_1))
            for line_event in line_path:
                line_1_transitions[line_event]._run(line_1)
                print(line_1.current_state)
                if (line_1.current_state.value) == "q1":
                    robot = Generator.create_master(robot_states, robot_transitions)
                    for robot_event in robot_path:
                        robot_transitions[robot_event]._run(robot)
                        print(robot.current_state)

        if supervisor.current_state.value == "line_2":
            # TODO: automata 3 (for) slave3
            line_2 = Generator.create_master(line_2_states, line_2_transitions)
            # print('\n' + str(packing))
            print("Executing path: {}".format(line_2))
            for line_event in line_path:
                line_2_transitions[line_event]._run(line_2)
                print(line_2.current_state)
                if (line_2.current_state.value) == "q1":
                    robot = Generator.create_master(robot_states, robot_transitions)
                    for robot_event in robot_path:
                        robot_transitions[robot_event]._run(robot)
                        print(robot.current_state)

        if supervisor.current_state.value == "stop":
            # TODO: automata 5 (for) slave3
            ...
            print("Supervisor done!")
        if supervisor.current_state.value == "error":
            # TODO: automata 6 (for) slave3
            ...
            print("Error!")

