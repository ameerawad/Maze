import random
import sys
from PIL import Image, ImageDraw
sys.setrecursionlimit(10000)
class Cell():
    def __init__(self, x, y):
        """"x and y are the corrdinates of the cell"""
        self.x = x # col number
        self.y = y # row number
        self.walls = {"up":True, "right":True, "down":True, "left":True} # True = wall exists
    def has_all_walls(self):
        """returns False if at least one wall is down"""
        return all(self.walls.values())
    def knock_down_wall(self, other, wall):
        """
        wall can be up, right, down, or left
        wall should be direction of main cell wall to be broken
        other should be cell opject
        """
        wall_pairs = {"up" : "down", "down" : "up", "right" : "left", "left" : "right"}
        self.walls[wall] = False # wall should be direction of main cell wall to be broken
        # still need to knock down other wall
        other.walls[wall_pairs[wall]] = False # other should be cell opject

    def get_coordinate(self):
        return (self.x, self.y)

class Maze():
    def __init__(self, nx, ny, cell_size=100, startX=1, startY=1):
        """nx and ny are the dimensions of the maze"""
        self.nx = nx # width
        self.ny = ny # height
        self.startX = startX
        self.startY = startY
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)] # array of cells with height and rows inverted
        self.cell_size = cell_size

    def cell_at(self, x, y):
        """returns the cell object at the x and y coordinate"""
        return self.maze_map[x][y]

    def find_valid_neighbors(self, cell):
        """
        cell is the opject cell that we want the neighbors for
        returns a list of possible neighbors to break walls and enter
        """
        delta = [("up", (0, -1)),
                 ("right", (1, 0)),
                 ("down", (0, 1)),
                 ("left", (-1, 0))] # array height and width are flipped and so y = x
        neighbors = [] # the list of neighbors to append
        for direction, (dx, dy) in delta:
            neighborX = cell.x + dx
            neighborY = cell.y + dy
            if (0 <= neighborX < self.nx) and (0 <= neighborY < self.ny): # makes sure we are not leaving the maze space
                potential_neighbor = self.cell_at(neighborX, neighborY)
                if potential_neighbor.has_all_walls(): # makes sure that the cell has not already been visited
                    neighbors.append((direction, potential_neighbor)) # example: ("up", Cell(x, y))
        return neighbors

    def find_neighbor_paths (self, cell):
        delta = {"up" : (0, -1),
                 "right" : (1, 0),
                 "down" : (0, 1),
                 "left" : (-1, 0)}
        empty_path_options = []
        for key in cell.walls:
            if cell.walls[key] == False:
                empty_path_options.append((cell.x + delta[key][0], cell.y + delta[key][1]))
        return empty_path_options # returns a list of tupules of each being an x and y coordinate

    def difficulty_finder(self):
        return

    def make_maze_graph (self):
        """
        returns a dictionary of all the cells in the maze
        keys of the dictionary are tuples of the cell coordinate (x, y)
        value of a key is a list of tuple coordinates of possible paths

        each key is a node (vertex)
        each value is an arc (edge)
        """
        maze_graph = {}
        for row in self.maze_map:
            for cell in row:
                maze_graph[cell.get_coordinate()] = self.find_neighbor_paths(cell)
        return maze_graph

    def find_next_to_visit(self, cell_location, visited_path):
        empty_paths = self.find_neighbor_paths(cell_location)
        for itm in empty_paths:
            if self.cell_at(itm[0], itm[1]) in visited_path:
                empty_paths.remove(itm)
        return empty_paths



    def maze_solution(self, map, nodes_visited, node, solutions = []):
        """
        creates a list of lists of all the solutions at the node
        maze solution is the path with the most number of nodes with decisions (i.e. 3 or 4 paths)
        returns a list of lists of all possible paths
        """
        # node is cell object
        # next_to_visit is a list of coordinate tuples potential possible nodes to visit
        # points_visited is a list of visited nodes
        all_solutions = solutions
        current_location = node
        points_visited = nodes_visited.copy() # takes a list of all node objects visited


        points_visited.append(current_location)
        next_to_visit = self.find_next_to_visit(current_location, points_visited) # gets the list of tupules possible paths

        # if next to visit is length:
        #   0 - we are at a dead we need to save the list of nodes as a solution
        #   1 - we are on a straight path and just need to keep going (recursive calls are not executed)
        #   2 - we are at an intersection and need to recusively call the solution of one of the nodes

        while len(next_to_visit) == 1: # loop ends when we reach dead end (len is 0) or a choice point (len is 1)
            # keep going straight
            update_location = next_to_visit.pop() # goes straight
            current_location = self.cell_at(update_location[0], update_location[1])
            points_visited.append(current_location)
            next_to_visit = self.find_next_to_visit(current_location, points_visited)
            # then goes back and checks if the new nextnext_to_visit is 1 or not
        if len(next_to_visit) == 0:
            # dead end is reached and we need to copy our path as a solusolutions
            a_solution = []
            for k in points_visited:
                a_solution.append(k.get_coordinate())
            # solution now has a list of coordinates as a possible paths
            all_solutions.append(a_solution)
            return all_solutions

        elif len(next_to_visit) >= 2:
            # we are at a node and so, we need to pick a path and solve it
            for p in next_to_visit:
                next_update = p # next is the path chosen
                next_node = self.cell_at(next_update[0], next_update[1])
                all_solutions_of_chosen_path = self.maze_solution(map, points_visited, next_node, all_solutions)
            all_solutions = all_solutions_of_chosen_path
            return all_solutions
        # if current_location == self.cell_at(self.startX, self.startY):


    def get_best_solution_path(self, map, nodes_visited, node):
        solutions_list = self.maze_solution(map, nodes_visited, node)
        longest_path_dictionary = {}
        for s in solutions_list:
            count = 0
            for cell in s:
                num_of_neighbors = len(self.find_neighbor_paths(self.cell_at(cell[0], cell[1])))
                if num_of_neighbors >= 3:
                    count += 1
            if str(count) in longest_path_dictionary.keys():
                longest_path_dictionary[str(count)].append(s)
            else:
                longest_path_dictionary[str(count)] = [s]
        kys = list(longest_path_dictionary.keys())
        for k in range(len(kys)):
            kys[k] = int(kys[k])
        kys.sort()
        solution = longest_path_dictionary[str(kys[-1])]

        if len(solution) == 1:
            return solution[0]
        elif len(solution) > 1:
            best_solution = []

            # 1: Most choices (hardest) becomes the solution
            most_choices = {}
            for s1 in solution:
                num_4 = 0
                for cell1 in s1:
                    num_of_neighbors1 = len(self.find_neighbor_paths(self.cell_at(cell[0], cell[1])))
                    if num_of_neighbors1 == 4:
                        num_4 += 1
                if str(num_4) in most_choices.keys():
                    most_choices[str(num_4)].append(s1)
                else:
                    most_choices[str(num_4)] = [s1]
            kys1 = list(most_choices.keys())
            for k1 in kys1:
                k1 = int(k1)
            kys1.sort()
            best_solution = most_choices[str(kys1[-1])]
            if len(best_solution) == 1:
                return best_solution[0]

            # 2: longest distance traveled becomes the solution
            longest_solutions = []
            length = -1
            for l in best_solution:
                if len(l) > length:
                    longest_solutions = [l]
                    length = len(l)
                elif len(l) == length:
                    longest_solutions.append(l)
            best_solution = longest_solutions
            if len(best_solution) == 1:
                return best_solution[0]

            # 3: just pick randomly
            a_choice = random.choice(best_solution)
            best_solution = [a_choice]
            if len(best_solution) == 1:
                return best_solution[0]

        print("If you reached here, something went wrong. FIX")

    def put_solution_in_image(self, solution):
        maze_image = Image.open("maze1.png")
        name_of_maze_solution = "maze1s"
        draw = ImageDraw.Draw(maze_image)
        half_cell = (self.cell_size//2)
        for p in range(len(solution[:-1])):
            start_point = ((solution[p][0]*self.cell_size)+half_cell, (solution[p][1]*self.cell_size)+half_cell)
            end_point = ((solution[p+1][0]*self.cell_size)+half_cell, (solution[p+1][1]*self.cell_size)+half_cell)
            draw.line([start_point, end_point], fill=(255,0,0), width=5)
        maze_image.save(name_of_maze_solution+".png")

    def put_maze_in_image(self, solution):
        endX = solution[-1][0]
        endY = solution[-1][1]
        name_of_maze = "maze1"
        mazeImg = Image.new("RGB", (self.nx*self.cell_size, self.ny*self.cell_size), color = (255, 255, 255))
        draw = ImageDraw.Draw(mazeImg)
        draw.line(((self.startX*self.cell_size, self.startY*self.cell_size),(self.startX*self.cell_size + self.cell_size, self.startY*self.cell_size + self.cell_size)), fill=(0,255,0), width=5)
        draw.line(((endX*self.cell_size, endY*self.cell_size),(endX*self.cell_size + self.cell_size, endY*self.cell_size + self.cell_size)), fill=(0,0,255), width=5)
        for row in self.maze_map:
            for cell in row:
                tl_point = (cell.x*self.cell_size, cell.y*self.cell_size)
                for key in cell.walls:
                    if cell.walls[key] == True:
                        if key == "up":
                            draw.line(((tl_point),(tl_point[0]+self.cell_size,tl_point[1])), fill=0)
                        if key == "right":
                            draw.line(((tl_point[0]+self.cell_size, tl_point[1]),(tl_point[0]+self.cell_size,tl_point[1]+self.cell_size)), fill=0)
                        if key == "down":
                            draw.line(((tl_point[0], tl_point[1]+self.cell_size),(tl_point[0]+self.cell_size,tl_point[1]+self.cell_size)), fill=0)
                        if key == "left":
                            draw.line(((tl_point),(tl_point[0],tl_point[1]+self.cell_size)), fill=0)
        mazeImg.save(name_of_maze+".png")

    def make_maze(self):
        total_number_cells = self.nx * self.ny
        current_cell = self.cell_at(self.startX, self.startY)
        cell_stack = []
        number_of_visited_cells = 1
        while number_of_visited_cells < total_number_cells: # while there are still cells to discover
            cell_neighbors = self.find_valid_neighbors(current_cell)
            if not cell_neighbors:
                current_cell = cell_stack.pop()
                continue # returns program to beggening of while loop
            direction, next_cell = random.choice(cell_neighbors)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            number_of_visited_cells += 1
        graph = self.make_maze_graph()
        start_cell = self.cell_at(self.startX, self.startY)
        solution = self.get_best_solution_path(graph, [], start_cell)
        self.put_maze_in_image(solution)
        self.put_solution_in_image(solution)
        print("Done")



myMaze = Maze(100, 100)
myMaze.make_maze()
