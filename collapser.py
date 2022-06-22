import numpy as np
import copy

class collapser:

    def __init__(self, ss = None,entrlist = None):
        if entrlist:
            self.l = copy.deepcopy(entrlist)
            return

        """
        Converts string to sudoku entropy list\n
        by collapsing every given point
        ex:\n
        N 1 N N 8 9 2 N N \n
        N 8 N N N 5 N 3 N \n
        N 9 N N N N N 7 N \n
        N N 6 N N 2 N 4 N \n
        N N 5 4 N N 7 N N \n
        N N N 9 7 N N N N \n
        N N N N N N N N N \n
        N N 3 N N 8 N 2 N \n
        N 5 N N N 4 N N 1 \n
        \n
        """
        tl = list(map(lambda x: x.split(" ")[:-1],ss.split("\n")))[:-1]
        self.l = np.array(np.zeros((9,9))).tolist() #i was so frustrated, that should be considered as a crime
        for j in range(len(self.l)):
            for i in range(len(self.l[j])):
                self.l[j][i] = [1,2,3,4,5,6,7,8,9]
        for y, row in enumerate(tl):
            for x, elem in enumerate(row):
                if elem != "N":
                    
                    self.collapse((x,y),int(elem))

    def collapse_single(self) -> list:
        for i in range(9):
            for j in range(9):
                if type(self.l[i][j]) is list:
                    if len(self.l[i][j]) == 1:
                        self.collapse( (j, i),self.l[i][j][0])

    def collapse(self, coord: tuple, n: int) -> list:
        x0, y0 = coord
        if type(self.l[y0][x0]) is list:

            if n in self.l[y0][x0]:
                self.l[y0][x0] = n
            else: return self
            
            ## for every row
            for i in range(9):
                #l[i][x0]
                if type(self.l[i][x0]) is list:
                    if n in self.l[i][x0]:
                        self.l[i][x0].remove(n)
            ## for every element in a home row
            for i in range(9):
                if type(self.l[y0][i]) is list:
                    if n in self.l[y0][i]:
                        self.l[y0][i].remove(n)   
            ## checks dedicated square
            sqx, sqy = x0 // 3 * 3, y0 // 3 * 3
            for y in range(sqy ,sqy + 3):
                for x in range(sqx , sqx + 3):
                    if type(self.l[y][x]) is list and int(n) in self.l[y][x]:
                        self.l[y][x].remove(n)

        self.collapse_single()
        return self
    def colour_sud(self) -> str:
        """
        Prints out colourful sudoku\n
        Takes as input entropy list (collapser.l)
        """
        ss = ""
        for row in self.l:
            for element in row:
                if type(element) is int:
                    ss += str("\033[1;35;40m")+str(element)+str("\033[0m") + " "
                else: ss += "N "
            ss += "\n"
        print (ss)
        return ss
def find_min_entropy(l: list) -> list:
    """
    Finds the lowest entropy and returns its coordinates\n
    Takes a whole entropy list as input
    
    result -> [(x, y), [n1, n2, n3]]
    """
    global_min = [1,1,1,1,1,1,1,1,1,1]
    coords_min = ()
    for y, row in enumerate(l):
        for x, elem in enumerate(row):
            if type(elem) is list:
                if len(elem) <= len(global_min):
                    global_min = elem
                    coords_min = x,y
    return [coords_min, global_min]
def get_status(l: list) -> int:
    """
    Takes sudoku entropy list as input\n
    returns -1 if its unsolvable AKA failed\n
    returns 1 if its solved\n
    returns 0 if none above aka still in progress
    """
    entr = 0
    for y, row in enumerate(l):
        for x, elem in enumerate(row):
            if type(elem) is list:
                if len(elem) == 0: return -1
                else: entr += 1
    if entr == 0: return 1
    return 0

def solver(ohmygodihatemutations: list):
    initial = copy.deepcopy(ohmygodihatemutations)
    """
    Provides a recursive solution for sudoku problem
    """
    status  = get_status(initial)
    match status:
        case -1:
            return 0
        case 1:
            return initial
        case 0:
            
            pos, values = find_min_entropy(initial)
            h = list(map(lambda value: solver((collapser(entrlist=initial).collapse(pos, value)).l), values))
            h = list(filter(bool, h))

            if h:
                return h[0]
            else:
                return 0

with open("test.txt", "r") as f:
    data = f.read()
init = collapser(ss = data)
init.colour_sud()
init = collapser(entrlist = solver(init.l))
init.colour_sud()