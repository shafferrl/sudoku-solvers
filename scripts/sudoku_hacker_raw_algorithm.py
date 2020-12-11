"""====================== Raw Algorithm ========================

This is a sudoku-solving algorithm developed a while back stripped
of any GUI or console-based user input so that the code can be made
agnostic to the user interface.

To use:

A SudokuSolver class is instantiated taking a dictionary as an argument
to its constructor with the keys of the dictionary having the last two
characters representing the row and column (i.e. "cell_01" -- 0 is the
first row, 1 is the second column).  Dictionary values must be integers
from 1 to 9 or their string representations (i.e. "5" and 5 are both
acceptable values), following standard numeric 9 x 9 sudoku format.

The "attempt_solve" method is called on the SudokuSolver object to
attempt to formulate a solution and returns a dictionary with the keys
in the same format they are received.

"""

class SudokuSolver:
    # Variable that keeps tally of numbers entered
    numberofentries = 0
    # Declare and initialize primary data structures used by solver algorithm
    num_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
    puzzle_list = [[0 for c in range(9)] for r in range(9)]
    # Declare the data structures and functions that will be referenced and updated when the puzzle is solving

    # Declare dictionary of possible coordinates of each number.  Will be populated with input coordinates after
    # functions are defined to preclude function definitions from being included in puzzle solution timer
    poss_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
    # List of solved coordinates
    solved_coords = []
    # Keep dictionary of coords the solver manages to solve for
    solver_solved = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
    # Keep count of how many values are solved
    amt_solved = 0
    # Declare and initialize dictionary that only retains newly solved numbers
    newNum_dict = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
    # Declare variable that counts how many coordinates will have been eliminated from possibilities by following function
    new_elims = 0
    # Keep list of coordinate sets that have been guessed from to try to solve puzzle
    guessSets = []
    # Keep a list of how many times each set of guess possibilities has been iterated on
    guessAmt = []
    # Keep a list of (lists of) coordinates eliminated while dependent on a guess
    guessDependElim = []
    # Declare boolean that indicates whether there are any guessed values
    is_guess = False
    # Declare boolean that indicates whether a guess set has been exhausted, which causes the program 
    # to revisit the set before it and iterate, assuming a wrong guess was further back in the chain of 
    # guesses than the set whose possibilities were just exhausted before the program could complete
    setExhausted = False
    
    # Constuctor method
    def __init__(self, form_data):
        self.numbers = form_data
        self.convert_fronttoback()
        self.check_initial_conflict()

    # Check whether conflict before attempting solve
    def check_initial_conflict(self):
        for no in self.num_dict:
            for coord in self.num_dict[no]:
                if self.isOnlyinRow(no, coord, self.num_dict) or self.isOnlyinCol(no, coord, self.num_dict) or self.isOnlyinBox(no, coord, self.num_dict):
                    pass
                else:
                    print(no, ' ', coord)
                    raise ValueError('Puzzle Input Conflict')
        
    # Define function that takes the information from data structures used by the solver and
    # transfers the information to data structures used to generate puzzle GUI
    def convert_backtofront(self):
        self.numberofentries = 0
        for num in self.num_dict:
            for crd in self.num_dict[num]:
                self.puzzle_list[crd[0]][crd[1]] = num
                absindx = crd[1]%3 + 3*(crd[0]%3) + 9*(int(crd[1]/3)) + 27*(int(crd[0]/3))
                numbers[absindx][0].set(num)
                numbers[absindx][1].set(str(num))
                self.numberofentries += 1
                if crd in self.solver_solved[num]:
                    buttons[absindx] = ttk.Button(buttonrowframes[int(absindx/3)], style="P1.P2.TButton", width=2, textvariable=numbers[absindx][1],
                                                      command = lambda n= numbers[absindx][0], s= numbers[absindx][1]: numinc(n,s))
                elif crd not in solver_solved[num]:
                    buttons[absindx] = ttk.Button(buttonrowframes[int(absindx/3)], style="P2.TButton", width=2, textvariable=numbers[absindx][1],
                                                      command = lambda n= numbers[absindx][0], s= numbers[absindx][1]: numinc(n,s))
                    
    # Take user-entered data and transfer it into data structures more useful to solver
    def convert_fronttoback(self):
        for cell in self.numbers:
            if self.numbers.get(cell):
                self.num_dict[int(self.numbers[cell])].append((int(cell[-2]), int(cell[-1])))
                self.numberofentries += 1
        for num in self.num_dict:
            for num_crd in self.num_dict[num]:
                self.puzzle_list[num_crd[0]][num_crd[1]] = num
    

    # Declare the 3 x 3 boxes used as units in the puzzle
    b1 = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)]
    b2 = [(3,0), (4,0), (5,0), (3,1), (4,1), (5,1), (3,2), (4,2), (5,2)]
    b3 = [(6,0), (7,0), (8,0), (6,1), (7,1), (8,1), (6,2), (7,2), (8,2)]
    b4 = [(0,3), (1,3), (2,3), (0,4), (1,4), (2,4), (0,5), (1,5), (2,5)]
    b5 = [(3,3), (4,3), (5,3), (3,4), (4,4), (5,4), (3,5), (4,5), (5,5)]
    b6 = [(6,3), (7,3), (8,3), (6,4), (7,4), (8,4), (6,5), (7,5), (8,5)]
    b7 = [(0,6), (1,6), (2,6), (0,7), (1,7), (2,7), (0,8), (1,8), (2,8)]
    b8 = [(3,6), (4,6), (5,6), (3,7), (4,7), (5,7), (3,8), (4,8), (5,8)]
    b9 = [(6,6), (7,6), (8,6), (6,7), (7,7), (8,7), (6,8), (7,8), (8,8)]
    boxes = [b1, b2, b3, b4, b5, b6, b7, b8, b9]

    # Define functions that assess input conflict
    def isRowConflict(self, puz_number, coord_tuple):
        for coords in range(len(self.num_dict[puz_number])):
                for coord in range(len(self.num_dict[puz_number][coords])):
                    if coord_tuple[0] == self.num_dict[puz_number][coords][0]:
                        return True
                    else: continue
        return False

    def isColConflict(self, puz_number, coord_tuple):
        for coords in range(len(self.num_dict[puz_number])):
                for coord in range(len(self.num_dict[puz_number][coords])):
                    if coord_tuple[1] == self.num_dict[puz_number][coords][1]:
                        return True
                    else: continue
        return False

    def isBoxConflict(self, puz_number, coord_tuple):
        for b in range(9):
            if coord_tuple in self.boxes[b]:
                for coords in range(len(self.boxes[b])):
                    if puz_number == self.puzzle_list[self.boxes[b][coords][0]][self.boxes[b][coords][1]]:
                        return True
                    else: continue
            else: continue
        return False

    # Consolidate input conflict-type functions into single function
    def isInputConflict(self, puz_number, coord_tuple):
        # Check to see if there is already a number at the index entered
        if self.puzzle_list[coord_tuple[0]][coord_tuple[1]] != 0:
            return 1
        # Check columns and rows
        if self.isRowConflict(puz_number, coord_tuple) or self.isColConflict(puz_number, coord_tuple):
            return 2
        # Check 3x3 boxes
        if self.isBoxConflict(puz_number, coord_tuple):
            return 3
        return 0

    # Resolve any input conflict into single yes/no rather than distinguishing by type
    # This will be cleaner in instances where the type of conflict need not be known
    def isAnyConflict(self, puz_number2, coord_tuple2):
        
        if self.isInputConflict(puz_number2, coord_tuple2) == 1:
            return True
        if self.isInputConflict(puz_number2, coord_tuple2) == 2:
            return True
        elif self.isInputConflict(puz_number2, coord_tuple2) == 3:
            return True
        return False

    # Define function that determines if a possible coordinate for a given number is the only possible coordinate in its respective row
    def isOnlyinRow(self, puz_no, poss_coord, check_dict):
        for coord in check_dict[puz_no]:
            if coord != poss_coord and coord[0] == poss_coord[0] or self.isAnyConflict(puz_no, poss_coord) and check_dict is not self.num_dict:
                return False
            else: continue
        return True

    # Define function that deterrmines if a possible coordinate for a given number is the only possible coordinate in its respective column
    def isOnlyinCol(self, puz_no, poss_coord, check_dict):
        for coord in check_dict[puz_no]:
            if coord != poss_coord and coord[1] == poss_coord[1] or self.isAnyConflict(puz_no, poss_coord) and check_dict is not self.num_dict:
                return False
            else: continue
        return True

    # Define function that determines if a possible coordinate for a given number is the only possible coordinate it its respective 3 x 3 box
    def isOnlyinBox(self, puz_no, poss_coord, check_dict):
        for box in self.boxes:
            if poss_coord in box:
                for coord in check_dict[puz_no]:
                    if coord != poss_coord and coord in box or self.isAnyConflict(puz_no, poss_coord) and check_dict is not self.num_dict:
                        return False
                    else: continue
        return True

    # Define function that combines "isOnly" functions into a single function that loops through all possibilities,
    # determines if there are any solutions, and updates the relevant data structure if (a) solution(s) is/are found
    def onlyOnes(self):
        for p_no in self.poss_dict:
            for pd_coord in self.poss_dict[p_no]:
                if self.isOnlyinRow(p_no, pd_coord, self.poss_dict) or self.isOnlyinCol(p_no, pd_coord, self.poss_dict) or self.isOnlyinBox(p_no, pd_coord, self.poss_dict):
                    self.num_dict[p_no].append(pd_coord)
                    self.puzzle_list[pd_coord[0]][pd_coord[1]] = p_no
                    self.newNum_dict[p_no].append(pd_coord)
                    self.solved_coords.append(pd_coord)
                    self.solver_solved[p_no].append(pd_coord)
                    self.amt_solved += 1
                    self.new_elims += 1
                else: continue
            for new_num in self.newNum_dict:
                for new_coord in self.newNum_dict[new_num]:
                    for pnum in self.poss_dict:
                        for pcoord in self.poss_dict[pnum]:
                            if new_coord in self.poss_dict[pnum]:
                                self.poss_dict[pnum].remove(new_coord)
                                if self.is_guess:
                                    self.guessDependElim[-1].append((pnum, new_coord))
                            else: continue

    # Define function that eliminates possibilities if there is a conflict with solved numbers
    def directConflictElim(self):
        for num in self.poss_dict:
            np_cds = []
            for po_cd in self.poss_dict[num]:
                if self.isAnyConflict(num, po_cd):
                    np_cds.append(po_cd)
            for np_cd in np_cds:
                self.poss_dict[num].remove(np_cd)
                if self.is_guess:
                    self.guessDependElim[-1].append((num, np_cd))
                self.new_elims += 1
                
    # Define function that selects a number and set of coordinates to use as guesses in the puzzle
    def newGuessSet(self):
        num_poss_list = []
        guess_options = []
        
        # Make list of numbers that still need to be solved and how many potential coordinates
        # there are for each number
        for num in self.poss_dict:
            if len(self.poss_dict[num]) > 1:
                num_poss_list.append((len(self.poss_dict[num]), num))
            else: continue
                    
        # Use the number with the minimum number of possibilites to increase chances of guessing correctly
        try_num = min(num_poss_list)[1]

        # Find the element (3x3 box, row, column) that contains the least number of possibilities from which to take a guess
        for trycrd in self.poss_dict[try_num]:
            # Check which boxes have multiple possibilities
            for box in range(len(self.boxes)):
                if trycrd in self.boxes[box]:
                    box_crds = [trycrd]
                    for otherboxcrd in self.poss_dict[try_num]:
                        if otherboxcrd != trycrd and otherboxcrd in self.boxes[box] and otherboxcrd not in box_crds:
                            box_crds.append(otherboxcrd)
                    if len(box_crds) > 1:
                        guess_options.append((len(box_crds), box_crds))
            # Check which rows have multiple possibilities
            for row in range(len(self.puzzle_list)):
                if row == trycrd[0]:
                    row_crds = [trycrd]
                    for otherrowcrd in self.poss_dict[try_num]:
                        if otherrowcrd != trycrd and otherrowcrd[0] == row and otherrowcrd not in row_crds:
                            row_crds.append(otherrowcrd)
                    if len(row_crds) > 1:
                        guess_options.append((len(row_crds), row_crds))
            # Check which columns have multiple possibilities
            for col in range(len(self.puzzle_list)):
                if col == trycrd[1]:
                    col_crds = [trycrd]
                    for othercolcrd in self.poss_dict[try_num]:
                        if othercolcrd != trycrd and othercolcrd[1] == col and othercolcrd not in col_crds:
                            col_crds.append(othercolcrd)
                    if len(col_crds) > 1:
                        guess_options.append((len(col_crds), col_crds))

        guess_elmnt = (try_num, min(guess_options)[1])
        # Find the row, box, or column from which to take a guess based on least number of possibilities
        self.guessAmt.append(1)
        self.guessSets.append(guess_elmnt)
        self.guessDependElim.append([])
        for elcrd in guess_elmnt[1]:
            if elcrd in self.poss_dict[try_num]:
                self.poss_dict[try_num].remove(elcrd)
                self.guessDependElim[-1].append((try_num, elcrd))
            else: continue
        self.num_dict[try_num].append(guess_elmnt[1][0])
        self.solver_solved[try_num].append(guess_elmnt[1][0])
        self.puzzle_list[guess_elmnt[1][0][0]][guess_elmnt[1][0][1]] = try_num
        self.solved_coords.append(guess_elmnt[1][0])
        self.newNum_dict[try_num].append(guess_elmnt[1][0])
        self.new_elims += len(guess_elmnt[1])
        self.amt_solved += 1

    # Define function that determines how to take a guess if it's needed to solve the puzzle
    def guessIt(self):
        self.is_guess = True
        poss_count = sum(len(self.poss_dict[no]) for no in self.poss_dict)
        # If the puzzle remains unsolved because no solution could be isolated from possibilities
        if len(self.solved_coords) < 81 and poss_count > 1 and not self.setExhausted:
            self.newGuessSet()
        # If the solver 'locked up' because a previous guess (in potentially a chain of guesses)
        # was incorrect:
        elif len(self.solved_coords) < 81 and poss_count == 0 or self.setExhausted:
            # If all possibilities from a set of guesses haven't been tried
            if self.guessAmt[-1] < len(self.guessSets[-1][1]):
                self.setExhausted = False
                # Re-add coordinates removed from pool of possibilities based on last guess to pool
                # and remove numbers solved in puzzle based on last guess from puzzle
                for guesstup in self.guessDependElim[-1]:
                    for pnum in self.poss_dict:
                        if guesstup[0] == pnum and guesstup[1] not in self.poss_dict[pnum]:
                            self.poss_dict[pnum].append(guesstup[1])
                    for num in self.num_dict:
                        if self.puzzle_list[guesstup[1][0]][guesstup[1][1]] == num:
                            self.num_dict[num].remove(guesstup[1])
                            self.solver_solved[num].remove(guesstup[1])
                            self.solved_coords.remove(guesstup[1])
                            self.amt_solved -= 1
                    self.puzzle_list[guesstup[1][0]][guesstup[1][1]] = 0
                # Select next coordinate from the guess set and use that as guess
                self.guessAmt[-1] += 1
                self.num_dict[self.guessSets[-1][0]].append(self.guessSets[-1][1][self.guessAmt[-1]-1])
                self.solver_solved[self.guessSets[-1][0]].append(self.guessSets[-1][1][self.guessAmt[-1]-1])
                self.amt_solved += 1
                for setcrd in self.guessSets[-1][1]:
                    if setcrd in self.poss_dict[self.guessSets[-1][0]]:
                        self.poss_dict[self.guessSets[-1][0]].remove(setcrd)
                        self.guessDependElim[-1].append((self.guessSets[-1][0], setcrd))
                self.puzzle_list[self.guessSets[-1][1][self.guessAmt[-1]-1][0]][self.guessSets[-1][1][self.guessAmt[-1]-1][1]] = self.guessSets[-1][0]
                self.solved_coords.append(self.guessSets[-1][1][self.guessAmt[-1]-1])
                self.newNum_dict[self.guessSets[-1][0]].append(self.guessSets[-1][1][self.guessAmt[-1]-1])
                self.new_elims += len(self.guessSets[-1][1]) 
            # If all possibilities from a set of guesses have been tried and the puzzle 'locks up',
            # it means a previous guess in the chain was wrong, since one coordinate in the set
            # had to be the correct one.  The last set must be deleted and the previous one revisited
            else:
                self.setExhausted = True
                # First, add possibilites removed from that set back to possible coordinates
                # and remove values from the puzzle that were based on that set of guesses.
                for guesstup in self.guessDependElim[-1]:
                    for pnum in self.poss_dict:
                        if guesstup[0] == pnum and guesstup[1] not in self.poss_dict[pnum]:
                            self.poss_dict[pnum].append(guesstup[1])
                    for num in self.num_dict:
                        if self.puzzle_list[guesstup[1][0]][guesstup[1][1]] == num:
                            self.num_dict[num].remove(guesstup[1])
                            self.solver_solved[num].remove(guesstup[1])
                            self.solved_coords.remove(guesstup[1])
                            self.amt_solved -= 1
                    self.puzzle_list[guesstup[1][0]][guesstup[1][1]] = 0
                # Next, remove the entire previous set of guesses, so the set before it can be
                # revisited the next time the loop goes around
                self.guessAmt.pop(-1)
                self.guessSets.pop(-1)
                self.guessDependElim.pop(-1)
                self.new_elims = 1
        # If puzzle is finished, solve any remaining value and exit solver loop
        else:
            self.onlyOnes()
            self.new_elims = 0

    # Define function that runs loop calling solver functions.  Function provides
    # error message if user has entered too few values into puzzle
    def attempt_solve(self):
        # Keep list of coordinates for which the number in that coordinate is solved.
        for num in self.num_dict:
            for scrd in self.num_dict[num]:
                if scrd not in self.solved_coords:
                    self.solved_coords.append(scrd)
        # Number of starting inputs
        start_amt = len(self.solved_coords)
        # Start solve by immediately eliminating coordinates as possibilities that conflict with
        # starting numbers by row, column, and 3x3 box
        for num in self.poss_dict:
            for r in range(len(self.puzzle_list)):
                for c in range(len(self.puzzle_list[r])):
                    if not self.isAnyConflict(num, (r, c)):
                            self.poss_dict[num].append((r, c))
        # Loop through, updating puzzle and other relevant data structures until no new coordinates are eliminated
        # (Indicates that puzzle is either solved, unsolvable, or not solvable via currently included methods)     
        its = 0
        while its < 1 or self.new_elims > 0 and its < 5000:
            self.new_elims = 0
            self.newNum_dict = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
            self.onlyOnes()
            self.directConflictElim()
            if self.new_elims == 0:
                self.guessIt()
            its += 1
        self.onlyOnes()
        #convert_backtofront()
