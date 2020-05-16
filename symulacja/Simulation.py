import numpy as np

from symulacja.commands.moves import  move_j

def position(number, steps):

    if number == 0:

        print("q_0 = Oczekiwanie na sygnał startu z sterownika")
        initialize = [ 90.0, 90.0, 0.0, 0.0, 0.0, 0.0 ]
        return initialize

    if number == 1:
        print("q_1 = Uruchomienie robota")
        start = [ 90.0, 90.0, 0.0, 0.0, 0.0, 0.0 ]
        return start

    if number == 2:
        print("q_2 = Podjechanie końcówki robota do obiektu")
        To_Object = [ 90.0, 90.0, 30.0, 0.0, 0.0, 0.0 ]
        return To_Object

    if number == 3:
        print("q_3 = Uruchomienie ssawki")
        Catch_Object = [ 90.0, 150.0, 30.0, 0.0, 0.0, 0.0 ]
        return Catch_Object

    if number == 4:
        print("q_4 = Przniesienie obiektu na nowe miejsce")
        Move_Object = [ 90.0, 90.0, 30.0, 0.0, 45.0, 0.0 ]
        return Move_Object

    if number == 5:
        print("q_5 = Wyłącznie ssawki")
        Put_Object = [ 0.0, 135.0, 0.0, 0.0, 45.0, 0.0 ]
        return Put_Object

    if number == 6:
        print("q_6 =  Powrót robota do pozycji początkowej")
        To_Start_Position = [ 0.0, 90.0, 30.0, 0.0, 45.0, 0.0 ]
        return To_Start_Position

    if number == 7:
        print("q_7 =  Wysłanie sygnału o błędzie do sterownika")
        error = steps[len(steps)-1]
        return error

    if number == 8:
        print("q_8 =  Przejście w tryb oczekiwania na wciśnięcie przycisku restart")
        wait_mode = steps[len(steps)-1]
        return wait_mode

def run(steps,robot):

    moves=[]

    for i in range(len(steps)):
        if i == len(steps) - 1:
            move = move_j(robot, steps[len(steps) - 1], steps[0])
        else:
            move = move_j(robot, steps[i], steps[i + 1])
        moves.append(move)

    Path = moves[0]

    for i in range(len(moves)-1):
        Path = np.concatenate((Path, moves[i+1]), axis=0)

    # animate robot
    robot.animate(stances=Path, frame_rate=30, unit='deg')







