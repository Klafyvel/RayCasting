#! /usr/bin/python3
import math
import random

from blocks import *

# mur ouvert :
#     BIT0 : gauche
#     BIT1 : droite
#     BIT2 : haut
#     BIT3 : bas

# Possible : 
#     0b0000 -> tout fermé (0)
#     0b0001 -> mur gauche ouvert (1)
#     0b0010 -> mur droit ouvert (2)
#     0b0011 -> mur gauche et droit ouvert (3)
#     0b0100 -> mur haut ouvert (4)
#     0b0101 -> mur haut et gauche ouvert (5)
#     0b0110 -> mur haut et droit ouvert (6)
#     0b0111 -> mur haut et gauche et droit ouvert (7)
#     0b1000 -> mur bas ouvert (8)
#     0b1001 -> mur bas et gauche ouvert (9)
#     0b1010 -> mur bas et droit ouvert (10)
#     0b1011 -> mur bas et droit et gauche ouvert (11)
#     0b1100 -> mur haut et bas ouvert (12)
#     0b1101 -> mur haut et bas et gauche ouvert (13)
#     0b1110 -> mur haut et bas et droit ouvert (14)
#     0b1111 -> tout ouvert (15)
S = 50

def is_same(l):
    for i in l:
        if i != l[0]:
            return False
    return True
def fusion(work_map, cell_type_a, cell_type_b):
    if cell_type_a == -1 or cell_type_b == -1 or cell_type_a==cell_type_b:
        return False
    new_val = cell_type_a
    old_val = cell_type_b
    for i in range(len(work_map)):
        for j in range(len(work_map[i])):
            if work_map[i][j] == old_val:
                work_map[i][j] = new_val
    return True

def fusion_laby(size):
    w,h = size
    work_map = [[i for i in range(w*j,w*(j+1))] for j in range(h)]
    returned_map = [[0]*w for i in range(h)]
    same = False
    while not same:
        x = random.randint(0,w-1)
        y = random.randint(0,h-1)
        op = 1 << random.randint(0,3)
        pos_type = work_map[y][x]
        impacted_type = -1
        impacted_x = x
        impacted_y = y
        if op&0b0001 and x>0:
            impacted_x = x-1
        elif op&0b0010 and x<len(work_map[y])-1:
            impacted_x = x+1
        elif op&0b0100 and y>0:
            impacted_y = y-1
        elif op&0b1000 and y<len(work_map)-1:
            impacted_y = y+1
        impacted_type = work_map[impacted_y][impacted_x]
        good_fus = fusion(work_map, pos_type, impacted_type)
        if good_fus:
            returned_map[y][x] |= op
            if op&0b0001:
                returned_map[impacted_y][impacted_x] |= 0b0010
            elif op&0b0010:
                returned_map[impacted_y][impacted_x] |= 0b0001
            elif op&0b0100:
                returned_map[impacted_y][impacted_x] |= 0b1000
            elif op&0b1000:
                returned_map[impacted_y][impacted_x] |= 0b0100
        same = is_same(work_map)
    return returned_map

def to_ray_map(lab):
    returned = [[wall((255,255,0))]*(len(lab)*2+2)]
    for i in lab:
        r = [wall((255,255,0))]
        n = [wall((255,255,0))]
        for j in i:
            r.append(EMPTY)
            if not j & 0b0010 :
                r.append(wall((random.randint(0,255), random.randint(0,255), random.randint(0,255))))
            else :
                r.append(EMPTY)
            if not j & 0b1000:
                n.append(wall((random.randint(0,255), random.randint(0,255), random.randint(0,255))))
            else:
                n.append(EMPTY)
            if n[-1] and r[-1]:
                n.append(EMPTY)
            else:
                n.append(wall((random.randint(0,255), random.randint(0,255), random.randint(0,255))))
        r.append(wall((255,255,0)))
        n.append(wall((255,255,0)))
        returned.append(r)
        returned.append(n)
    returned.append([[wall((255,255,0))]*(len(lab)*2+2)])
    return returned

def laby(size):
    return to_ray_map(fusion_laby(size))