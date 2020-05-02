import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout, to_agraph
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

G = nx.MultiDiGraph()

G.add_node("IDLE")

G.add_edge("IDLE", "IDLE", transition = 'idle')
G.add_edge("IDLE", "PACKING", transition = 'packing')
G.add_edge("PACKING", "PICK_AND_PLACE_1", transition = 'line_1')
G.add_edge("PACKING", "ERROR", transition = 'error_packing')
G.add_edge("PICK_AND_PLACE_1", "PICK_AND_PLACE_2", transition = 'line_2')
G.add_edge("PICK_AND_PLACE_1", "ERROR", transition = 'error_l1')
G.add_edge("PICK_AND_PLACE_2", "WRAPPER", transition = 'wrapper')
G.add_edge("PICK_AND_PLACE_2", "ERROR", transition = 'error_l2')
G.add_edge("WRAPPER", "STOP", transition = 'stop')
G.add_edge("STOP", "STOP", transition = 'check_stop')
G.add_edge("WRAPPER", "ERROR", transition = 'error_wrapper')
G.add_edge("ERROR", "ERROR", transition = 'error')

G_pack = nx.MultiDiGraph()

G_pack.add_node("PACKING")

G_pack.add_edge("PACKING", "P1", transition = 'idle_packing')
G_pack.add_edge("P1", "P2", transition = 'p1p2')
G_pack.add_edge("P1", "ERROR_PACKING", transition = 'p1_error')
G_pack.add_edge("P2", "P3", transition = 'p2p3')
G_pack.add_edge("P2", "ERROR_PACKING", transition = 'p2_error')
G_pack.add_edge("P3", "P4", transition = 'p3p4')
G_pack.add_edge("P3", "ERROR_PACKING", transition = 'p3_error')
G_pack.add_edge("P4", "P5", transition = 'p4p5')
G_pack.add_edge("P4", "ERROR_PACKING", transition = 'p4_error')
G_pack.add_edge("P5", "P5", transition = 'p5p5')
G_pack.add_edge("ERROR_PACKING", "RESTART_PACKING", transition = 'error_p7')
G_pack.add_edge("ERROR_PACKING", "ERROR_PACKING", transition = 'error_error')
G_pack.add_edge("RESTART_PACKING", "P1", transition = 'p7p1')
G_pack.add_edge("RESTART_PACKING", "RESTART_PACKING", transition = 'p7p7')

G_line = nx.MultiDiGraph()

G_line.add_node("PICK_AND_PLACE_1")
G_line.add_node("PICK_AND_PLACE_2")
G_line.add_edge("PICK_AND_PLACE_2", "L1", transition = 'idle_line')
G_line.add_edge("PICK_AND_PLACE_1", "L1", transition = 'idle_line')
G_line.add_edge("L1", "L2", transition = 'l1l2')
G_line.add_edge("L1", "ERROR_L", transition = 'l1_error')
G_line.add_edge("L2", "L3", transition = 'l2l3')
G_line.add_edge("L2", "ERROR_L", transition = 'l2_error')
G_line.add_edge("L3", "L4", transition = 'l3l4')
G_line.add_edge("L4", "L4", transition = 'l4l4')
G_line.add_edge("L3", "ERROR_L", transition = 'l3_error')
G_line.add_edge("ERROR_L", "RESTART_LINE", transition = 'error_l6')
G_line.add_edge("ERROR_L", "ERROR_L", transition = 'error_error')
G_line.add_edge("RESTART_LINE", "RESTART_LINE", transition = 'l6l6')
G_line.add_edge("RESTART_LINE", "L1", transition = 'l6l1')


G_robot = nx.MultiDiGraph()

G_robot.add_node("P1")
G_robot.add_node("P3")
G_robot.add_node("L1")
G_robot.add_edge("P1", "R1", transition = 'p1r1')
G_robot.add_edge("P3", "R1", transition = 'p3r1')
G_robot.add_edge("L1", "R1", transition = 'l1r1')
G_robot.add_edge("R1", "R2", transition = 'r1r2')
G_robot.add_edge("R1", "ERROR_ROBOT", transition = 'r1_error')
G_robot.add_edge("R2", "R3", transition = 'r2r3')
G_robot.add_edge("R2", "ERROR_ROBOT", transition = 'r2_error')
G_robot.add_edge("R3", "R4", transition = 'r3r4')
G_robot.add_edge("R3", "ERROR_ROBOT", transition = 'r3_error')
G_robot.add_edge("R4", "R5", transition = 'r4r5')
G_robot.add_edge("R4", "ERROR_ROBOT", transition = 'r4_error')
G_robot.add_edge("R5", "R6", transition = 'r5r6')
G_robot.add_edge("ERROR_ROBOT", "RESTART_ROBOT", transition = 'error_rest')
G_robot.add_edge("ERROR_ROBOT", "ERROR_ROBOT", transition = 'error_error')
G_robot.add_edge("RESTART_ROBOT", "R1", transition = 'rest_r1')
G_robot.add_edge("RESTART_ROBOT", "RESTART_ROBOT", transition = 'restart')

F= nx.compose_all([G,G_pack,G_line,G_robot])

print(F.nodes)

F.graph['edge'] = {'arrowsize': '0.6', 'splines': 'curved'}
F.graph['graph'] = {'scale': '4'}

A = to_agraph(F)
A.layout('dot')
A.draw('Graph.png')
img =mpimg.imread('Graph.png')
imgplot = plt.imshow(img)
plt.axis('off')

plt.show()
