# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 22:04:50 2019

@author: yashc
"""
# import all the necessary modules
from operator import attrgetter
import time
import os
import psutil


# initialize global lists
open_list = []   
closed_list = []
moves= []
parent = []
goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0] # representation of goal node
# Indices of a 2D 4*4 grid
two_d_index = [[0,0], [0,1], [0,2], [0,3], [1,0], [1,1], [1,2], [1,3], [2,0], [2,1], [2,2], [2,3], [3,0], [3,1], [3,2], [3,3]]


# Node class will be used to create our objects
class Node:
    def __init__(self, state = None, parent = None, move = None, g_n = None, h_n = None, f_n = None):
        self.state = state      # current state
        self.parent = parent        # parent state
        self.move = move        # Move required to reach current state
        self.g_n = g_n      # Cost from root node to current node
        self.h_n = h_n      # Heuristic value
        self.f_n = f_n      # Sum of g(n) and h(n)
  
    
# Main function or starting point of the program      
def main():
    global moves
    global parent
    ip = input("Enter input state: ")
    in_list = list(map(int, ip.split()))  # List input is taken
    global open_list
    global closed_list
    misplaced_heuristic(in_list[:])     # for a-star with no. of misplaced tiles
    open_list.clear()
    closed_list.clear()
    moves.clear()
    parent.clear()
    manhattan_heuristic(in_list[:])     # for a-star with manhattan distance
        
        
def misplaced_heuristic(in_list):       # for a-star with no. of misplaced tiles
    start1 = time.time()
    root  = Node(in_list, None, None, 0, None)  # Create root node object
    root.h_n = no_misplaced_tiles(root.state)
    root.f_n = root.g_n + root.h_n
    open_list.append(root)
    if check_goal(root, 'a'):
        return
    while len(open_list) > 0:       
        cur_node = min(open_list, key = attrgetter('f_n'))  # Finds the object with minimum f(n) 
        if check_goal(cur_node, 'a'):
            moves.append(cur_node.move)
            parent = cur_node.parent
            while parent != None:
                for node in closed_list:
                    if node.state == parent:
                        moves.append(node.move)
                        parent = node.parent
            del moves[len(moves)-1]
            movesp = ''.join(moves[::-1])
            # Print the output if a solution is found
            print("Goal State Found!\n")
            print("A-Star for Number of Misplaced Tiles heuristic:")
            print("Moves: ",movesp)
            print("Number of Nodes Expanded: ", len(closed_list))
            end1 = time.time()
            print("Time Taken:", end1 - start1, "seconds")
            process = psutil.Process(os.getpid())
            print("Memory Used:", process.memory_info().rss / 1000, "kb\n\n")
            break
        
        
def manhattan_heuristic(in_list):       # for a-star with manhattan distance
    start2 = time.time()
    root  = Node(in_list, None, None, 0, None)
    root.h_n = manhattan_distance(root.state)
    root.f_n = root.g_n + root.h_n
    open_list.append(root)
    if check_goal(root, 'b'):
        return
    while len(open_list) > 0:
        cur_node = min(open_list, key = attrgetter('f_n'))      # Finds the object with minimum f(n)
        if check_goal(cur_node, 'b'):
            moves.append(cur_node.move)
            parent = cur_node.parent
            while parent != None:
                for node in closed_list:
                    if node.state == parent:
                        moves.append(node.move)
                        parent = node.parent
            del moves[len(moves)-1]
            movesp = ''.join(moves[::-1])
            # Print the output if a solution is found
            print("A-Star for Manhattan Distance heuristic: ")
            print("Moves: ",movesp)
            print("Number of Nodes Expanded: ", len(closed_list))
            end2 = time.time()
            print("Time Taken:", end2 - start2, "seconds")
            process = psutil.Process(os.getpid())
            print("Memory Used:", process.memory_info().rss / 1000, "kb")
            break
        
        
def no_misplaced_tiles(cur_state):  # returns the no. of misplaced tiles
    misplaced = 0
    for i in range(0, 15):
        if cur_state[i] != i + 1:
            misplaced += 1
    return misplaced


def manhattan_distance(cur_state):  # returns the manhattan distance
    man_dist = 0
    for x in cur_state:
        if x == 0:
            continue
        i = cur_state.index(x)
        j = goal.index(x)
        temp_row = abs(two_d_index[i][0] - two_d_index[j][0])
        temp_col = abs(two_d_index[i][1] - two_d_index[j][1])
        man_dist = man_dist + temp_row + temp_col
    return man_dist


def check_goal(cur_node, z): # checks for goal, else creates children nodes
    if cur_node.state == goal:
        return True
    else:
        open_list.remove(cur_node)
        closed_list.append(cur_node)
        i = cur_node.state.index(0) # find index of '0'
        left(cur_node, i, z)
        right(cur_node, i, z)
        up(cur_node, i, z)
        down(cur_node, i, z)
        
        
def check_if_visited(cur_node): # checks if node is already visited
    # c and o are flags to check if node already exists in given lists
    c = False;
    o = False;
    for x in closed_list:
        if x.state == cur_node.state:
            c = True
            if x.g_n > cur_node.g_n:    # if new g(n) is smaller, replace the node in closed list
                closed_list.remove(x)
                closed_list.append(cur_node)
    for y in open_list:
        if y.state == cur_node.state:
            o = True
            if y.g_n > cur_node.g_n:    # if new g(n) is smaller, replace the node in open list
                open_list.remove(y)
                open_list.append(cur_node)
    if c != True and o != True:
        open_list.append(cur_node)
           
        
def left(cur_node, i, z):   # performs left-shift operation
    if i not in {0, 4, 8, 12}:  # skips if 0 is already on extreme left
        child_node = Node()
        child_node.parent = cur_node.state[:]
        temp = cur_node.state[:]
        temp[i-1], temp[i] = temp[i], temp[i-1]
        child_node.state = temp[:]
        child_node.move = 'L'
        child_node.g_n = cur_node.g_n + 1
        if z == 'a':    # Calculate heuristic depending upon the function running
            child_node.h_n = no_misplaced_tiles(child_node.state)
        elif z == 'b':
            child_node.h_n = manhattan_distance(child_node.state)
        child_node.f_n = child_node.g_n + child_node.h_n
        check_if_visited(child_node)
        
        
def right(cur_node, i, z):  # performs right-shift operation
    if i not in {3, 7, 11, 15}: # skips if 0 is already on extreme right
        child_node = Node()
        child_node.parent = cur_node.state[:]
        temp = cur_node.state[:]
        temp[i+1], temp[i] = temp[i], temp[i+1]
        child_node.state = temp[:]
        child_node.move = 'R'
        child_node.g_n = cur_node.g_n + 1
        if z == 'a':    # Calculate heuristic depending upon the function running
            child_node.h_n = no_misplaced_tiles(child_node.state)
        elif z == 'b':
            child_node.h_n = manhattan_distance(child_node.state)
        child_node.f_n = child_node.g_n + child_node.h_n
        check_if_visited(child_node)
        
        
def up(cur_node, i, z): # performs up-shift operation
    if i not in {0, 1, 2, 3}:       # skips if 0 is already on extreme top
        child_node = Node()
        child_node.parent = cur_node.state[:]
        temp = cur_node.state[:]
        temp[i-4], temp[i] = temp[i], temp[i-4]
        child_node.state = temp[:]
        child_node.move = 'U'
        child_node.g_n = cur_node.g_n + 1
        if z == 'a':    # Calculate heuristic depending upon the function running
            child_node.h_n = no_misplaced_tiles(child_node.state)
        elif z == 'b':
            child_node.h_n = manhattan_distance(child_node.state)
        child_node.f_n = child_node.g_n + child_node.h_n
        check_if_visited(child_node)
        
        
def down(cur_node, i, z):   # performs down-shift operation
    if i not in {12, 13, 14, 15}:   # skips if 0 is already on extreme bottom
        child_node = Node()
        child_node.parent = cur_node.state[:]
        temp = cur_node.state[:]
        temp[i+4], temp[i] = temp[i], temp[i+4]
        child_node.state = temp[:]
        child_node.move = 'D'
        child_node.g_n = cur_node.g_n + 1
        if z == 'a':    # Calculate heuristic depending upon the function running
            child_node.h_n = no_misplaced_tiles(child_node.state)
        elif z == 'b':
            child_node.h_n = manhattan_distance(child_node.state)
        child_node.f_n = child_node.g_n + child_node.h_n
        check_if_visited(child_node)
        
        
if __name__=="__main__": main()


    
