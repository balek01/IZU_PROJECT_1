from enum import Enum
import math
import sys
import os
import time


open = []
close = []
pom = []
path = []
MAP = False
OUTS = True
PPATH = True
DEBUG = True
BENCH = False


class Node:
    def __init__(self, position, b, g, h, f, parent):
        self.position = position
        self.b = b
        self.g = g
        self.h = h
        self.f = f
        self.parent = parent


if BENCH:
    START = (1, 1)
    END = (13, 13)
    mat = [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1,  5,  3, -1, -1, -1,  1, -1,  1,  5,  1, -1,  3, -1, -1],
        [-1,  6, -1,  1,  7, -1,  1,  1, -1,  4, -1,  4,  8,  2, -1],
        [-1,  1,  6, -1, -1,  1, -1, -1, -1,  1,  1, -1, -1, -1, -1],
        [-1, -1,  5,  5, -1,  5, -1, -1, -1, -1, -1,  2,  5,  5, -1],
        [-1,  8, -1,  2, -1, -1, -1, -1, -1,  4, -1, -1,  8, -1, -1],
        [-1,  4,  2, -1,  3, -1,  1,  6, -1, -1, -1,  7, -1,  3, -1],
        [-1, -1,  5, -1, -1, -1,  7, -1, -1, -1, -1, -1, -1,  8, -1],
        [-1,  6, -1,  2, -1, -1, -1, -1, -1, -1, -1,  6,  1, -1, -1],
        [-1,  5, -1,  1,  6,  8, -1, -1,  7,  2, -1,  4, -1, -1, -1],
        [-1, -1,  4, -1, -1, -1,  8, -1, -1, -1,  4, -1, -1, -1, -1],
        [-1,  8, -1,  7, -1,  2, -1,  9, -1,  2, -1,  1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1,  5, -1, 9, -1,  7, -1,  3, -1, -1],
        [-1, -1, -1, -1,  4, -1, -1, -1, -1, -1, -1, -1,  4,  3, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
else:
    START = (3, 7)
    END = (6, 3)
    mat = [[9, 9, 8, 9, 7, 3, 6, 7, 9, 9],
           [8, 7, 6, 9, 3, 9, 9, 9, 9, 8],
           [8, 7, 6, 9, 3, -1, -1, -1, 9, 8],
           [8, 7, 5, 8, 3, 5, 2, -1, 9, 6],
           [8, 5, 7, 8, 3, 4, 6, -1, 9, 7],
           [-1, -1, -1, -1, 3, -1, -1, -1, -1, -1],
           [9, 8, -1, 9, 9, 3, 8, -1, 9, 9],
           [7, 7, -1, 2, 4, 3, 9, -1, 9, 9],
           [7, 8, -1, 8, 7, 3, 9, -1, 9, 9],
           [8, 7, 7, 8, 9, 3, 9, 9, 9, 9]]

# transform ints to nodes
for y in range(len(mat)):
    for x in range(len(mat[0])):
        mat[y][x] = Node((x, y), mat[y][x], None, None, None, None)

iteration = 0
if OUTS: iteration += 1

if (OUTS == False):
    os.system('cls')

def field():
    global iteration
    print(f"\n\n\033[94mIteration: {iteration}.\033[0m")
    print("Map:")
    console_delete = True
    for y in range(len(mat)):
        for x in range(len(mat[0])):
            current: Node = mat[y][x]
            if current.b == -1:
                print(f" \033[91m{current.b}\033[0m", end=' |')
            elif (y == START[1] and x == START[0]) or (y == END[1] and x == END[0]):
                print(f"  \033[36m{current.b}\033[0m", end=' |')
            elif current in path:
                console_delete = False
                print(f"  \033[95m{current.b}\033[0m", end=' |')
            elif current in open:
                print(f"  \033[92m{current.b}\033[0m", end=' |')
            elif current in close:
                print(f"  \033[93m{current.b}\033[0m", end=' |')
            else:
                print(f"  {current.b}", end=' |')
        print("")
    if (OUTS == False) and console_delete:
        time.sleep(0.2)
        os.system('cls')
       


if MAP:
    field()
dx = START[0]-END[0]
dy = START[1]-END[1]
h = round(math.sqrt((dx)**2 + (dy)**2), 2)
g = mat[START[1]][START[0]].b
f = g + h
mat[START[1]][START[0]] = Node((START[0], START[1]), g, g, h, f, None)
open.append(mat[START[1]][START[0]])


def neigh(matrix, rowNumber, colNumber):
    result = []
    for colAdd in range(-1, 2):
        newCol = colNumber + colAdd
        if newCol >= 0 and newCol <= len(matrix)-1:
            for rowAdd in range(-1, 2):
                newRow = rowNumber + rowAdd
                if newRow >= 0 and newRow <= len(matrix)-1:
                    if newCol == colNumber and newRow == rowNumber:
                        continue
                result.append(matrix[newCol][newRow])
    return result


def out(open, close):
    global DEBUG
    global iteration
    if OUTS and not MAP: print(f"\n\n\033[94mIteration: {iteration}.\033[0m")
    print("Open: ")
    for o in open:
        if DEBUG:
            print(
                f"\033[92m{o.position}\033[0m, {o.b}, {o.g}, {o.h}, \033[1m{o.f}\033[0m, {o.parent}", end="\n")
        else:
            print(
                f"[\033[92m{o.position}\033[0m, \033[1m{o.f}\033[0m, {o.parent}]", end="\n")
    print("Close: ")
    for c in close:
        if DEBUG:
            print(
                f"\033[91m{c.position}\033[0m, {c.b}, {c.g}, {c.h}, \033[1m{c.f}\033[0m, {c.parent}", end="\n")
        else:
            print(
                f"[\033[91m{c.position}\033[0m, \033[1m{c.f}\033[0m, {c.parent}]", end="\n")
    return


def get_path():
    curr = mat[END[1]][END[0]]
    while True:
        path.append(curr)
        if curr.parent == None:
            break
        curr = mat[curr.parent[1]][curr.parent[0]]
    return path


def print_path_helptable(path):
    print(f"\n\n\033[94mPath:\033[0m", end="\n")
    for p in range(len(path)-1, -1, -1):
        p = path[p]

        print(
            f"<\033[91m{p.position}\033[0m {p.g}, \033[1m{p.f}\033[0m, {p.parent}>", end=" ")
    print(f"\n\n\033[94mHelp Table:\033[0m", end="\n")
    for p in pom:
        print(f"[\033[1m{p.position}\033[0m {p.g}, {p.h}, {p.f}]", end="\n")


if OUTS:
    out(open, close)

while True:
    iteration += 1
    current = None

    for o in open:
        if current == None or current.f > o.f:
            current = o

    open.remove(current)
    close.append(current)
    # found path
    if current.position == END:
        if OUTS:
            out(open, close)
        break

    neighbors = neigh(mat, current.position[0], current.position[1])

    for neighbor in neighbors:

        # wall or close skip
        if neighbor.b == -1 or neighbor in close:
            continue

        dx = neighbor.position[0] - END[0]
        dy = neighbor.position[1] - END[1]

        h = round(math.sqrt((dx)**2 + (dy)**2), 2)

        g = round(neighbor.b, 2) + current.g
        f = round(g+h, 2)

        if neighbor.f == None or f < neighbor.f or neighbor not in open:
            neighbor.h = h
            neighbor.f = f
            neighbor.g = g
            neighbor.parent = current.position
            pom.append(neighbor)
            if neighbor not in open:
                open.append(neighbor)
    if MAP:
        field()
    if OUTS:
        out(open, close)
path = get_path()
if MAP:
    field()
if PPATH:
    print_path_helptable(path)
