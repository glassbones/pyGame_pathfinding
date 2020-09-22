import math
import random
import pygame
from queue import PriorityQueue

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(precursors, current_cell, draw, counter):
    # traversing backwards through the dictionary starting at target
    # while the current_cell is in the path (we stop itterating at the start cell)
    while current_cell in precursors:
        # each cell stores its previous cell as a value in the dict
        current_cell = precursors[current_cell]
        current_cell.set_path()
        counter.increase_by(1)
        draw()

def algorithm(draw, grid, start, target, counter):
    count = 0
    # using priority que to prioritize smallest value inside the set
    open_set = PriorityQueue()
    # put = push ( API is dumb )
    # sequential argument explanation( F score , When item added to que (for tie breaker if F score tie) , Cell )
    open_set.put((0, count, start))
    # hash is to look inside open set.. priorityQueue is weird and only lets you remove stuff
    open_set_hash = {start} 
    # previous cell dict
    precursors = {} 
    g_score = {cell: float("infinity") for row in grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float("infinity") for row in grid for cell in row}
    f_score[start] = h(start.get_pos(), target.get_pos()) # estimated distance
   
    while not open_set.empty():
        # listen for quit event so user can close the app while algorithm is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # .get is poping the lowest value off the set
        current_cell = open_set.get()[2]
        open_set_hash.remove(current_cell)
        # if current is target we have reached our destination and need to draw the path
        if current_cell == target:
            reconstruct_path(precursors, target, draw, counter)
            # repainting the target cuz we drew over it
            target.set_target()
            return True
        # if current is not target consider neighbors of current cell
        for neighbor in current_cell.neighbors:
            # increment g score of all neighbors
            temp_g_score = g_score[current_cell] + 1
            # if new score is a better than old score
            # this path to the neighbor is cheaper than the previous path stored path
            if temp_g_score < g_score[neighbor]:
                # update path
                precursors[neighbor] = current_cell
                # update g score
                g_score[neighbor] = temp_g_score
                # update f score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), target.get_pos())
                # if neighbor isn't in open_set_hash 
                if neighbor not in open_set_hash:
                    # add it to the que
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_open()
        draw()
        # if the current cell we just considered is not the start node remove it from the set
        if current_cell != start:
            current_cell.set_closed()
    # return FALSE because we did not find the target :c
    return False

class Counter:
    def __init__(self, count):
        self.count = count
    def increase_by(self, num): self.count = self.count + num

def circuit_walk(path):
    print('circuit walk')
    seen = set(path)
    next_circuit_cell = []

    for neighbor in path[-1].neighbors:
        if not neighbor.is_branch:
            if neighbor not in seen:
                next_circuit_cell.append(neighbor)

    if next_circuit_cell == []: return path[-1]
    if len(next_circuit_cell) == 3: return circuit_compare(next_circuit_cell[0], next_circuit_cell[1], next_circuit_cell[2])
    if len(next_circuit_cell) == 2: return circuit_compare(next_circuit_cell[0], next_circuit_cell[1])
    if len(next_circuit_cell) == 1: return next_circuit_cell[0]

def circuit_compare(a, b, c = None):
    print('circuit_compare')
    lst = [a,b]
    if c: lst = [a,b,c]
    return random.choice(lst)
    """
    a_path = [a]
    b_path = [b]
    i = 0

    while len(a_path) != i and len(b_path) != i:
        a_next_circuit_cell = circuit_walk(a_path)
        b_next_circuit_cell = circuit_walk(b_path)

        if a_next_circuit_cell == a_path -1: 
            if c != None: return circuit_compare(a, c)
            else: return a
        if b_next_circuit_cell == b_path -1: 
            if c != None: return circuit_compare(b, c)
            else: return b
        
        a_path = a_path.append(a_next_circuit_cell)
        b_path = b_path.append(b_next_circuit_cell)
        i += 1
    """