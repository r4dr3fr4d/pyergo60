from pykeeb import *
from math import *

columns = 7
rows = 4

plate = Keyboard_matrix(rows, columns, 1.5, .5, 3, [0,0,12], 0, 5)

##left to right are columns 0 and up, bottom to up are rows 0 and up
plate.rm[3]=[0, 2, 7, 0, 0, 0]
plate.rm[2]=[0, 2.5, 4, 0, 0, 0]
plate.rm[1]=[0, 1.75, 4, -10, 0, 0]
plate.rm[0]=[0, 1, 6.5, -20, 0, 0]
plate.cm[0]=[0, -7, 0, 0, 0, 0] 
plate.cm[1]=[0, -2, 0, 0, 0, 0]
plate.cm[2]=[0, -2, 0, 0, 0, 0]
plate.cm[3]=[0, 5, -3, 0, 0, 0]
plate.cm[5]=[0, -10, 5, 0, 0, 0]
plate.cm[6]=[0, -10, 5, 0, 0, 0]
plate.im[1][0]=[0, 0, 2, 0, 0, 0]
plate.ik[0][0]=True
plate.generate()

#arc
arc_columns = 1
negative_arc_columns = 2
arc_rows = 1
arc_angle = 20
arc_length = DSA_KEY_WIDTH / (2 * sin(radians(arc_angle/2))) + 12 
z_arc = 5
z_length = DSA_KEY_WIDTH / (2 * sin(radians(z_arc/2))) + 40 

arc_origin = list(map(sum, zip(plate.switch_matrix[0][0].transformations[0][0:3], [-4, -1, 13]))) 
arc = Keyboard_arc(arc_columns, negative_arc_columns, arc_rows, arc_length, arc_angle, 0, 0, 2, 2, 3, arc_origin, 15, 4, 30)

#hulls connecting arc and matrix
conn_hulls = (arc.sm[0][2].get_corner('fr', .1, .1) + plate.sm[1][0].get_back()).hull()
conn_hulls += (arc.sm[0][2].get_front() + plate.sm[1][0].get_corner('bl', .1, .1)).hull()
conn_hulls += (arc.sm[0][2].get_right(.01, 0) + plate.sm[0][1].get_left()).hull()
conn_hulls += (arc.sm[0][2].get_right(.01, 0) + plate.sm[0][1].get_corner('fl', .1, .1, 0, -3) + plate.sm[0][1].get_corner('bl', .1, .1)).hull()
conn_hulls += project((arc.sm[0][2].get_corner('br', 2, 3, 2, 3) + plate.sm[0][1].get_corner('bl', .5, 3, 0, 3)).hull())
conn_hulls += project((arc.sm[0][2].get_corner('fl', .5, 3, 0, 3) + plate.sm[1][0].get_corner('bl', 3, .5, 3)).hull())
conn_hulls -= plate.sm[1][0].get_switch_at_location(True) #cuts part of hull that's near sm[1][0]'s switch hole
arc.front_wall[2].disable()
arc.right_wall[0].disable()
arc.front_right_corner.disable()

keys = arc.sm[0][2].get_keycap(True)
keys += arc.sm[0][1].get_keycap(True)
keys += arc.sm[0][0].get_keycap(True)
keys += plate.sm[1][0].get_keycap(True)
keys += plate.sm[0][1].get_keycap()
keys += plate.sm[1][1].get_keycap()
keys += plate.sm[2][1].get_keycap()
keys += plate.sm[3][1].get_keycap()
keys += plate.sm[0][2].get_keycap()
keys += plate.sm[1][2].get_keycap()
keys += plate.sm[2][2].get_keycap()
keys += plate.sm[3][2].get_keycap()

keys2 = plate.sm[0][6].get_keycap()
keys2 += plate.sm[1][6].get_keycap()
keys2 += plate.sm[2][6].get_keycap()
keys2 += plate.sm[3][6].get_keycap(True)
keys2 += plate.sm[3][5].get_keycap(True)
keys2 += plate.sm[3][4].get_keycap(True)
keys2 += plate.sm[3][3].get_keycap(True)

switches = plate.sm[1][3].get_keyswitch()  
switches += plate.sm[1][2].get_keyswitch()
switches += plate.sm[0][1].get_keyswitch()
switches += plate.sm[0][1].get_keyswitch()

cable_hole = Cylinder(30, 7, center=True).rotate([90,0,0])
cable_hole = (cable_hole + cable_hole.translate([10,0,0])).hull().translate([26,70,0]).color("Blue")
right_hand = conn_hulls + arc.get_arc() + plate.get_matrix() - cable_hole
left_hand = right_hand.mirror([1,0,0])
(left_hand).write("pyergo60_left.scad")
(right_hand).write("pyergo60_right.scad")
#(right_hand.translate([50,0,0]) + left_hand.translate([-50,0,0])).write("pyergo60.scad")
