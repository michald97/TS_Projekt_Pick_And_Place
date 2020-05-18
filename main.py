from automaty.packing_slave import *
from automaty.line_1 import *
from automaty.line_2 import *
from automaty.robot import *
from automaty.master import *
from klasy.generator import *
from grafy.graph import *
from symulacja.Simulation import *

import argparse
import robopy.base.model as robot
import sys

parser = argparse.ArgumentParser()
parser.add_argument("model", help="Model of robot (puma / orion)")
args = parser.parse_args()

sim = []

if str(args.model).lower() == "puma":
    model = robot.Puma560()
elif str(args.model).lower() == "orion":
    model = robot.Orion5()
else:
    print("Bad model specified. Try again.")
    sys.exit()


def statemachine():
    # create paths from transitions (exemplary)
    path_1 = ["m_0_1", "m_1_2", "m_2_3", "m_3_4", "m_4_5", "m_5_0"]
#     path_2 = ["m_0_1", "m_1_2", "m_2_3", "m_3_4", "m_4_6", "m_6_5", "m_5_0"]
#     path_3 = ["m_0_1", "m_1_2", "m_2_3", "m_3_6", "m_6_5", "m_5_0"]
#     path_4 = ["m_0_1", "m_1_2", "m_2_6", "m_6_5", "m_5_0"]
#     path_5 = ["m_0_1", "m_1_6", "m_6_5", "m_5_0"]
    paths = [path_1]

    packing_path = ["p_0_1", "p_1_2", "p_2_3", "p_3_6", "p_6_6", "p_6_7", "p_7_1", "p_1_2", "p_2_3", "p_3_4", "p_4_5",
                    "p_5_0"]
    robot_path = ["r_0_1", "r_1_2", "r_2_3", "r_3_4", "r_4_5", "r_5_6","r_6_0"]
    line_path = ["l_0_1", "l_1_2", "l_2_3", "l_3_4"]

    def run_robot():
        robot = Generator.create_master(robot_states, robot_transitions)
        print("Executing path: {}".format(robot_path))
        steps = []
        for i, robot_event in enumerate(robot_path):
            if robot_event == "r_0_1":
                step = position(0, steps)
                steps.append(step)
                robot_transitions[robot_event]._run(robot)
                print(robot.current_state)
            if robot_event == "r_1_2":
                step = position(1, steps)
                steps.append(step)
                robot_transitions[robot_event]._run(robot)
                print(robot.current_state)
            if robot_event == "r_2_3":
                step = position(2, steps)
                steps.append(step)
                robot_transitions[robot_event]._run(robot)
                print(robot.current_state)
            if robot_event == "r_3_4":
                step = position(3, steps)
                steps.append(step)
                robot_transitions[robot_event]._run(robot)
                print(robot.current_state)
            if robot_event == "r_4_5":
                step = position(4, steps)
                steps.append(step)
                robot_transitions[robot_event]._run(robot)
                print(robot.current_state)
            if robot_event == "r_5_6":
                step = position(5, steps)
                steps.append(step)
                robot_transitions[robot_event]._run(robot)
                print(robot.current_state)
            if robot_event == "r_6_0":
                step = position(6, steps)
                steps.append(step)
                robot_transitions[robot_event]._run(robot)
                print(robot.current_state)
            if robot_event == "r_1_7" or robot_event == "r_2_7" or robot_event == "r_3_7" \
                    or robot_event == "r_4_7" or robot_event == "r_5_7":
                step = position(7, steps)
                steps.append(step)
                robot_transitions[robot_event]._run(robot)
                print(robot.current_state)
            if robot_event == "r_7_8":
                step = position(8, steps)
                steps.append(step)
                robot_transitions[robot_event]._run(robot)
                print(robot.current_state)
        run(steps, model) #run animation


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
                packing = Generator.create_master(packing_states, packing_transitions)
                print("Executing path: {}".format(packing_path))

                for packing_event in packing_path:
                    packing_transitions[packing_event]._run(packing)
                    print(packing.current_state)
                    if (packing.current_state.value) == "p1":
                        run_robot()

                    if (packing.current_state.value) == "p3":
                        run_robot()

            if supervisor.current_state.value == "line_1":
                line_1 = Generator.create_master(line_1_states, line_1_transitions)
                print("Executing path: {}".format(line_1))

                for line_event in line_path:
                    line_1_transitions[line_event]._run(line_1)
                    print(line_1.current_state)
                    if (line_1.current_state.value) == "q1":
                        run_robot()

            if supervisor.current_state.value == "line_2":
                line_2 = Generator.create_master(line_2_states, line_2_transitions)
                print("Executing path: {}".format(line_2))
                for line_event in line_path:
                    line_2_transitions[line_event]._run(line_2)
                    print(line_2.current_state)
                    if (line_2.current_state.value) == "q1":
                        run_robot()

            if supervisor.current_state.value == "stop":
                print("Supervisor done!")
            if supervisor.current_state.value == "error":
                print("Error!")



if __name__ == "__main__":
    search()
    display()
    print('\n')
    statemachine()
