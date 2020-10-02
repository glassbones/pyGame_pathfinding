import math
from os import startfile
import random
import pygame
from queue import PriorityQueue

class Pathing:
    def __init__(self, grid, start = None, target = None):
        self.grid = grid
        self.start = start
        self.target = target
        self.circuit_flag = start
        self.branch_flags = []
        self.counter = 0

    def reset_flags(self):
        self.circuit_flag = self.start
        self.branch_flags = []

    def h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, precursors, current_cell, draw):
        # traversing backwards through the dictionary starting at target
        # while the current_cell is in the path (we stop itterating at the start cell)
        while current_cell in precursors:
            # each cell stores its previous cell as a value in the dict
            current_cell = precursors[current_cell]
            current_cell.set_path()
            self.counter += 1
            draw()

    def algorithm(self, draw):
        count = 0
        # using priority que to prioritize smallest value inside the set
        open_set = PriorityQueue()
        # put = push ( API is dumb )
        # sequential argument explanation( F score , When item added to que (for tie breaker if F score tie) , Cell )
        open_set.put((0, count, self.start))
        # hash is to look inside open set.. priorityQueue is weird and only lets you remove stuff
        open_set_hash = {self.start} 
        # previous cell dict
        precursors = {} 
        g_score = {cell: float("infinity") for row in self.grid.cells for cell in row}
        g_score[self.start] = 0
        f_score = {cell: float("infinity") for row in self.grid.cells for cell in row}
        f_score[self.start] = self.h(self.start.get_pos(), self.target.get_pos()) # estimated distance
    
        while not open_set.empty():
            # listen for quit event so user can close the app while algorithm is running
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            # .get is poping the lowest value off the set
            current_cell = open_set.get()[2]
            open_set_hash.remove(current_cell)
            # if current is target we have reached our destination and need to draw the path
            if current_cell == self.target:
                self.reconstruct_path(precursors, self.target, draw)
                # repainting the target cuz we drew over it
                self.target.set_target()
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
                    f_score[neighbor] = temp_g_score + self.h(neighbor.get_pos(), self.target.get_pos())
                    # if neighbor isn't in open_set_hash 
                    if neighbor not in open_set_hash:
                        # add it to the que
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.set_open()
            draw()
            # if the current cell we just considered is not the start node remove it from the set
            if current_cell != self.start:
                current_cell.set_closed()
        # return FALSE because we did not find the target :c
        return False

    def circuit_walk(self, path):
        print('circuit walk')
        seen = set(path)
        next_circuit_cell = []

        for neighbor in path[-1].neighbors:
            if not neighbor.is_branch:
                if neighbor not in seen:
                    next_circuit_cell.append(neighbor)

        if next_circuit_cell == []: return path[-1]
        if len(next_circuit_cell) == 3: return self.circuit_compare(next_circuit_cell[0], next_circuit_cell[1], next_circuit_cell[2])
        if len(next_circuit_cell) == 2: return self.circuit_compare(next_circuit_cell[0], next_circuit_cell[1])
        if len(next_circuit_cell) == 1: return next_circuit_cell[0]

    def circuit_compare(self, a, b, c = None):
        print('circuit_compare')
        lst = [a,b]
        if c: lst = [a,b,c]
        return random.choice(lst)

    def navigate(self, grid, canvas):
        self.start.set_is_seen()
        grid.seen.add(self.start)
        print(f'self.start is {self.start.x} , {self.start.y}')
        # if branch flag at current position remove it
        self.branch_flags = [ _ for _ in self.branch_flags if _ != self.start ]
        # if 2 or more current neighbors are untraveled nodes branch flag here
        unseen = [neighbor for neighbor in self.start.neighbors if not neighbor.is_seen]
        if len(unseen) > 1: self.branch_flags.append(self.start)
        # if 2 or more current neighbors are untraveled circuit nodes circuit flag here
        unseen_circuit_cells = [neighbor for neighbor in unseen if not neighbor.is_branch and not neighbor.is_seen]
        if len(unseen_circuit_cells) > 1: self.circuit_flag = self.start

        # if no untraveled neighbors, self.target is last branch flag
        print(f'unseen = {[neighbor.x for neighbor in self.start.neighbors if not neighbor.is_seen]}')
        if unseen == []:
            if self.branch_flags != []:
                self.target = self.branch_flags[-1]
            elif self.branch_flags == []:
                # if no branch flag return to circuit flag
                if self.target != self.start:
                    self.target = self.circuit_flag
                # if current position is circuit flag maze should be complete ???????????
                if self.target == self.start:
                    print('this shouldn\'t print unless everything is explored') 

        # if any neighbor is untraveled branch node self.target is that node pick node farther from last circuit flag
        print(f'unseen = {[neighbor.x for neighbor in self.start.neighbors if not neighbor.is_seen]}')
        if unseen != []:
            unseen_branch_cells = [neighbor for neighbor in unseen if neighbor.is_branch]
            # this is not optimal, need a tie breaker function that travels shortest dead end first
            print(f'unseen branches = {[neighbor for neighbor in unseen if neighbor.is_branch]}')
            if unseen_branch_cells != []: self.target = unseen_branch_cells[0]
            else:
                print(f'unseen circuits = {[neighbor for neighbor in unseen if not neighbor.is_branch]}')
                # if any neighbor is untraveled circuit node self.target pick optimal path
                if len(unseen_circuit_cells) == 4: self.target = self.circuit_compare(self.circuit_compare(unseen_circuit_cells[0],unseen_circuit_cells[1]), self.circuit_compare(unseen_circuit_cells[2],unseen_circuit_cells[3]))
                if len(unseen_circuit_cells) == 3: self.target = self.circuit_compare(unseen_circuit_cells[0],unseen_circuit_cells[1],unseen_circuit_cells[2])
                if len(unseen_circuit_cells) == 2: self.target = self.circuit_compare(unseen_circuit_cells[0],unseen_circuit_cells[1])
                else: self.target = unseen_circuit_cells[0]

        if len(unseen) == 1: self.target = unseen[0]

        for row in grid.cells:
            for cell in row:
                cell.update_neighbors()
        print(f'self.target is {self.target.x} , {self.target.y}')
        self.algorithm(lambda: canvas.draw(grid))

        self.start = self.target
        self.start.is_start()
        self.target = None

    """
        
        d
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