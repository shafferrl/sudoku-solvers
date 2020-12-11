#%%
"""=================== Sudoku Solver v.1 ======================
Enter the initial values of each number in the Sudoku puzzle.
Enter the column and row value separated by a comma, respectively.
"0,0" corresponds to the upper left corner, "8,0" the upper right,
"0,8" the lower left, and "8,8" the lower right.
If you are done with the initial values for the number shown or
the number is not an initial/given value, type "done" to proceed
to the next number.
If you enter a number incorrectly, you can enter "undo", which will
remove the last coordinate input and continue from there.
Once you've entered all the initial values all the way through 9
and confirmed that they are correct, the solver will begin.
===================================================================
"""

# >> INPUT SETUP SECTION =====================================================

# Declare dictionary to associate puzzle numbers with coordinates they inhabit 
num_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}

# Declare and populate the 9 x 9 puzzle array with 'empty' indices ("0" as placeholder)
puzzle_list = []
for r in range(9):
    row = []
    for c in range(9):
        row.append(0)
    puzzle_list.append(row)
    

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
def isRowConflict(puz_number, coord_tuple):
    for coords in range(len(num_dict[puz_number])):
            for coord in range(len(num_dict[puz_number][coords])):
                if coord_tuple[0] == num_dict[puz_number][coords][0]:
                    return True
                else: continue
    return False

def isColConflict(puz_number, coord_tuple):
    for coords in range(len(num_dict[puz_number])):
            for coord in range(len(num_dict[puz_number][coords])):
                if coord_tuple[1] == num_dict[puz_number][coords][1]:
                    return True
                else: continue
    return False

def isBoxConflict(puz_number, coord_tuple):
    for b in range(9):
        if coord_tuple in boxes[b]:
            for coords in range(len(boxes[b])):
                if puz_number == puzzle_list[boxes[b][coords][0]][boxes[b][coords][1]]:
                    return True
                else: continue
        else: continue
    return False

# Combine all conflict types into one function
def isInputConflict(puz_number, coord_tuple):
    # Check to see if there is already a number at the index entered
    if puzzle_list[coord_tuple[0]][coord_tuple[1]] != 0:
        return 1
    # Check columns and rows
    if isRowConflict(puz_number, coord_tuple) or isColConflict(puz_number, coord_tuple):
        return 2
    # Check 3 x 3 boxes
    if isBoxConflict(puz_number, coord_tuple):
        return 3
    return 0

# Define function that combines conflict types into a single function that assesses whether there
# is any conflict at all.  This will be cleaner to use in solver functions where knowing the type of
# conflict is not important for eliminating coordinates as possibilities
def isAnyConflict(puz_number2, coord_tuple2):

    if isInputConflict(puz_number2, coord_tuple2) == 1:
        return True
    elif isInputConflict(puz_number2, coord_tuple2) == 2:
        return True
    elif isInputConflict(puz_number2, coord_tuple2) == 3:
        return True
    return False


# Function that prints Sudoku puzzle into Python shell
# in aesthetically pleasing / easy to read manner
def print_puzzle(puz_lst):

    for r in range(len(puz_lst)):
        row_print = '|  '
        for c in range(len(puz_lst[r])):
            if c == 2 or c == 5 or c == 8:
                if(puz_lst[r][c]) != 0:
                    row_print += str(puz_lst[r][c]) + '  |  '
                else:
                    row_print += '   |  '
            else:
                if(puz_lst[r][c]) != 0:   
                    row_print += str(puz_lst[r][c]) + '   '
                else:
                    row_print += '    '
        if r == 0:
            print(' ____ ___ ____'*3)
        if r == 0 or r == 3 or r == 6:
            print('|    |   |    '*3 + '|')
        else:
            print('|-   +   +   -'*3 + '|')
        print(row_print)
        if r == 2 or r == 5 or r == 8:
            print('|____|___|____'*3 + '|')

    
# >> INPUT RECEIVING AND HANDLING SECTION =======================================================================================================

#Obtain initial values from user
puz_num = 1
input_list = []

while puz_num <= 9:
    while True:

        # ---------------------------------------------------------------------
        # FOR DEBUGGING ONLY: Bypass user input (until "^ FOR DEBUGGING ONLY ^")
        '''
        #Two-star (out of five) difficulty (https://puzzles.usatoday.com/sudoku/, April 30, 2019):
        num_dict = {1: [(2,8), (6,6), (7,4)], 2: [(0,5), (3,0), (7,2), (8,4)], 3: [(0,4), (8,6), (5,8), (4,5)],
                    4: [(0,2), (1,4), (4,0), (7,1), (5,5)], 5: [(3,3), (4,1), (1,7)], 6: [(2,2), (4,3)], 7: [(4,8)],
                    8: [(1,6), (4,7), (8,2)], 9: [(0,6), (6,0), (8,3)]}
        
        #Three-star (out of five) difficulty (https://puzzles.usatoday.com/sudoku/, May 4, 2019)
        num_dict = {1: [(1,8),(4,6),(6,7),(7,1),(8,4)], 2: [(4,4),(7,0)], 3: [(0,7),(2,4),(3,0),(6,5)],
                    4: [(1,4),(4,2),(5,8),(7,6),(8,1)], 5: [(0,8),(2,1),(6,4)], 6: [(1,7),(4,1),(5,4),(8,0)],
                    7: [(1,2),(2,6),(4,7),(7,4)], 8: [(2,3),(3,4),(6,2),(7,8)], 9: [(1,0),(0,4)]}
        
        num_dict = {1: [(5, 3), (7, 7), (6, 2)], 2: [(2, 6)], 3: [(1, 2), (5, 7)],
                    4: [(4, 4), (8, 6)], 5: [(4, 5), (7, 3), (3, 1)], 6: [(1, 3), (6, 7)],
                    7: [(2, 1), (3, 5), (4,6)], 8: [(0, 0), (6, 8), (7, 2)], 9: [(2, 4), (8, 1)]}
        
        #Four-star (out of five) difficulty (https://puzzles.usatoday.com/sudoku/, May 2, 2019):
        num_dict = {1:[(2,6),(4,7),(5,4)], 2:[(1,0),(2,5),(4,1),(3,4)], 3:[(4,6),(6,3),(8,7)],
                    4:[(0,5),(7,4)], 5:[(2,1),(5,2),(4,4),(6,7)], 6:[(2,4),(1,8),(7,0),(8,3)],
                    7:[(3,5),(6,2)], 8:[(0,1),(1,4)], 9:[(3,6),(4,2),(5,3),(6,4),(7,8)]}
        
        #Five-star (out of five) difficulty (https://puzzles.usatoday.com/sudoku/, April 28, 2019):
        num_dict = {1:[(0,0),(4,6),(7,8)], 2:[(1,2),(5,1)], 3:[(1,3),(3,7),(7,5)],
                    4:[(0,5),(3,3),(2,7),(7,6),(8,4)], 5:[(0,4),(1,6)], 6:[(4,2),(6,1),(8,3)],
                    7:[(1,0),(2,6),(5,5),(7,2),(8,8)], 8:[(3,0),(1,5),(5,8)], 9:[(6,2),(7,3)]}
        
        #Four-star (out of five) difficulty (https://puzzles.usatoday.com/sudoku/, May 9, 2019):
        num_dict = {1:[(8,4)], 2:[(1,1),(5,0),(4,3),(7,4)], 3:[(0,4),(4,1),(5,8),(8,2),(7,7)],
                    4:[(2,7),(3,0),(4,5),(6,4)], 5:[(0,0),(2,4),(3,8),(5,5),(6,1),(8,3)], 6:[(2,2),(0,6),(8,7)],
                    7:[(0,5),(4,7),(6,6)], 8:[(0,1),(1,4),(3,3),(8,8)], 9:[]}
        
        #Five-star (out of five) difficulty (https://puzzles.usatoday.com/sudoku/, May 3, 2019):
        num_dict = {1:[(0,3),(2,1),(5,4)], 2:[(1,7),(3,1),(8,4),(7,8)], 3:[(0,0),(1,4),(5,5),(8,7)],
                    4:[(3,6),(5,3),(7,4),(8,8)], 5:[(0,5),(8,3)], 6:[(0,1),(3,4),(8,5)],
                    7:[(3,3),(5,7),(7,1)], 8:[(0,4),(5,2),(6,7)], 9:[(1,0),(3,5)]}
        
        #'Evil' difficulty (https://www.websudoku.com/?level=4, Evil Puzzle # 6,346,965,862)
        num_dict = {1:[(1,0),(5,2),(3,6),(4,5)], 2:[(4,0),(3,4),(1,2),(8,5)], 3:[(0,0),(4,3),(3,8)],
                    4:[(5,0),(6,3),(7,6),(2,4)], 5:[(0,3),(6,6),(4,8)], 6:[(2,5),(5,4),(8,7)],
                    7:[(2,2),(8,8)], 8:[(6,4)], 9:[(0,1),(7,8)]}
        
        #'Evil' difficulty (https://www.websudoku.com/?level=4, Evil Puzzle # 9,837,753,931)
        num_dict = {1:[(5,0),(2,1),(3,7),(8,6)], 2:[(0,4),(2,0),(6,8),(8,3)], 3:[(0,0),(3,2),(7,6)],
                    4:[(0,2),(3,8),(6,6)], 5:[(8,4)], 6:[(5,1),(4,5)],
                    7:[(1,2),(2,3),(6,7)], 8:[(2,2),(0,5),(8,8)], 9:[(4,3),(5,6),(6,5)]}
        '''
        #'Evil' difficulty (https://www.websudoku.com/?level=4, Evil Puzzle # Evil Puzzle 428,924,163)
        num_dict = {1:[(0,0),(2,6),(3,4)], 2:[(5,6),(8,3)], 3:[(1,8),(4,5),(7,4),(8,0)],
                    4:[(3,2),(5,4),(6,8),(7,0)], 5:[(0,8),(6,3),(8,2)], 6:[(0,6),(1,4)],
                    7:[(3,1),(4,3)], 8:[(2,5),(5,7),(8,8)], 9:[(2,0),(0,5),(6,2)]}
        '''
        num_dict = {1: [(0, 1),(2, 8),(5, 0),(6, 4),(8, 7)],2:[(1, 5),(4, 4),(8, 6)],3:[(1, 2),(2, 7),(8, 0)],
                    4: [(0, 6),(2, 4),(3, 8)],5:[(3, 5),(5, 1)],6:[(0, 2),(6, 0),(7, 6)],
                    7: [(7, 3)], 8: [(5, 3), (6, 1)], 9: [(0, 8), (3, 7), (8, 2)]}
        '''
        for no in num_dict:
            for crd in num_dict[no]:
                puzzle_list[crd[0]][crd[1]] = no
        puz_num = 10
        break
    
        # ^ FOR DEBUGGING ONLY ^
        # ---------------------------------------------------------------------


        if len(num_dict[puz_num]) >= 9: break
        coord_inp = input('Enter initial coordinates for ['+ str(puz_num)+ ']: ')
        if coord_inp.lower() == 'done':
            break

        # Undo if user makes mistake on previous coordinate input
        # "undo" can be repeated until all inputs have been erased
        elif coord_inp.lower() == 'undo':
            if len(input_list) < 1:
                print('\nNothing to undo!\n')
                continue
            while len(num_dict[puz_num]) < 1 and puz_num > 1:
                puz_num -= 1
                if len(num_dict[puz_num]) < 1: continue
                else: break
            # Update relevant data structures
            num_dict[puz_num].remove(input_list[len(input_list)-1][1])
            puzzle_list[input_list[len(input_list)-1][1][1]][input_list[len(input_list)-1][1][0]] = 0
            print('['+ str(puz_num) +'] removed from coordinate '+ str(input_list[len(input_list)-1][1]) + '.')
            input_list.pop(len(input_list)-1)

        # Gather coordinates
        else:
            try:
                if int(coord_inp[0]) >= 9 or int(coord_inp[2]) >= 9:
                    print('\nINPUT ERROR: Column and row indices must be between or inlude 0 and 8.')
                    continue
                user_tup = (int(coord_inp[0]), int(coord_inp[2]))
                puz_tup = (int(coord_inp[2]), int(coord_inp[0]))
                if isInputConflict(puz_num, puz_tup) == 1 or isInputConflict(puz_num, puz_tup) == 2 or isInputConflict(puz_num, puz_tup) == 3:
                    if isInputConflict(puz_num, puz_tup) == 1:
                        print('\nINPUT ERROR: There is already a number at that index.')
                    elif isInputConflict(puz_num, puz_tup) == 2:
                        print('''\nINPUT ERROR: According to Sudoku rules, each row and column
may not contain the same number more than once.''')
                    elif isInputConflict(puz_num, puz_tup) == 3:
                        print('''\nINPUT ERROR: According to Sudoku rules, 3 x 3 boxes
may not contain the same number more than once.''')
                    print('\nPlease retry input.')
                    continue
                input_list.append((puz_num, puz_tup))
                num_dict[puz_num].append(puz_tup)
                puzzle_list[puz_tup[0]][puz_tup[1]] = puz_num
            except:
                print('\nINPUT ERROR: Invalid input. \nPlease follow instructions in header.\n')
    puz_num += 1

isInFin = ''
isRetry = False

# Print out puzzle with numbers entered and change, add, or remove any as desired by the user
# Puzzle only prints out once or if changes are made and user returns to 'check level'
while isInFin.lower() != 'y':
    if isRetry == False:
        pass
    try:
        isInFin = input('\nAre the values in the puzzle correct? (Enter "y" or "n"): ')
        if isInFin.lower() != 'y' and isInFin.lower() != 'n':
            isRetry = True
            print("\nINPUT ERROR: Invalid input.  Let's try this again...")
            continue
        else:
            isRetry = True
            while isInFin.lower() == 'n':
                try:
                    inpChange = input('''\nEnter the number you'd like to add, change, or remove.
When you are finished making changes, enter "done": ''')
                    if inpChange.lower() == 'done':
                        isInFin == ''
                        break
                    elif int(inpChange) < 1 or int(inpChange) > 9:
                        print("\nINPUT ERROR: Input must be an integer between and including 1 and 9.")
                        continue
                    elif int(inpChange) >= 1 and int(inpChange) <= 9:
                        while True:
                            try:
                                coord_inp2 = input('''\nEnter the coordinates you'd either like to add [''' + str(inpChange) + '''] to
or remove [''' + str(inpChange) + '''] from (or "done" to exit to number selection): ''')
                                if coord_inp2.lower() == 'done':
                                    isRetry = False
                                    break
                                elif int(coord_inp2[0]) >= 9 or int(coord_inp2[2]) >= 9:
                                    print('\nINPUT ERROR: Column and row indices must be between or include 0 and 8.')
                                    print('\nRetry input.')
                                    continue
                                else:
                                    user_tup2 = (int(coord_inp2[0]), int(coord_inp2[2]))
                                    puz_tup2 = (int(coord_inp2[2]), int(coord_inp2[0]))
                                    puz_val2 = puzzle_list[puz_tup2[0]][puz_tup2[1]]
                                    if puz_val2 == int(inpChange):
                                        num_dict[int(inpChange)].remove(puz_tup2)
                                        puzzle_list[puz_tup2[0]][puz_tup2[1]] = 0
                                        print('\n[' + str(inpChange) + '] removed from ' + str(user_tup2) + '.')
                                        continue
                                    elif puz_val2 != int(inpChange) and puz_val2 != 0:
                                        if isInputConflict(int(inpChange), puz_tup2) == 2 or isInputConflict(int(inpChange), puz_tup2) == 3:
                                            if isInputConflict(int(inpChange), puz_tup2) == 2:
                                                print('''\nINPUT ERROR: According to Sudoku rules, each row and column
may not contain the same number more than once.''')
                                            elif isInputConflict(int(inpChange), puz_tup2) == 3:
                                                print('''\nINPUT ERROR: According to Sudoku rules, 3 x 3 boxes
may not contain the same number more than once.''')
                                            print('\nPlease retry input.')
                                            continue
                                        else:
                                            num_dict[int(inpChange)].append(puz_tup2)
                                            num_dict[puz_val2].remove(puz_tup2)
                                            print('\nYou have replaced [' + str(puz_val2) + '] with [' + str(inpChange) +
                                                  '] in ' + str(user_tup2) + '.')
                                            puzzle_list[puz_tup2[0]][puz_tup2[1]] = int(inpChange)
                                            continue
                                    else:
                                        if isInputConflict(int(inpChange), puz_tup2) == 2 or isInputConflict(int(inpChange), puz_tup2) == 3:
                                            if isInputConflict(int(inpChange), puz_tup2) == 2:
                                                print('''\nINPUT ERROR: According to Sudoku rules, each row and column
may not contain the same number more than once.''')
                                            elif isInputConflict(int(inpChange), puz_tup2) == 3:
                                                print('''\nINPUT ERROR: According to Sudoku rules, 3 x 3 boxes
may not contain the same number more than once.''')
                                            print('\nPlease retry input.')
                                            continue
                                        else:
                                            num_dict[int(inpChange)].append(puz_tup2)
                                            puzzle_list[puz_tup2[0]][puz_tup2[1]] = int(inpChange)
                                            print('\n[' + str(inpChange) + '] added to ' + str(user_tup2) + '.')
                                            continue
                            except:
                                print("\nINPUT ERROR: Invalid input.  Let's try this again...")
                                continue
                except:
                    print("\nINPUT ERROR: Invalid input.  Let's try this again...")
                    continue
    except:
        print("\nINPUT ERROR: Invalid input.  Let's try this again...")
        continue


# >> SOLVER SETUP SECTION ===================================================================================
        
# Start to solve the puzzle
# print('\nAttempting to solve puzzle...\n')

# Declare the data structures and functions that will be referenced and updated when the puzzle is solving.

# Declare dictionary of possible coordinates of each number.  Will be populated with input coordinates after
# functions are defined to preclude function definitions from being included in puzzle solution timer.
poss_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}

# Keep list of coordinates for which the number in that coordinate is solved.
solved_coords = []
for num in num_dict:
    for scrd in num_dict[num]:
        solved_coords.append(scrd)

start_amt = len(solved_coords)

# Keep dictionary of coords the solver manages to solve for.
solver_solved = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}


 # >> Basic Functions / Algorithms ---------------------------------------------------------------------------

# Project initial inputs or solved values into respective rows, columns, and boxes
# and eliminate possibilities based on 'hard' solutions.

# Keep count of how many values are solved.
amt_solved = 0

# Define function that determines if a possible coordinate for a given number is the only possible coordinate in its respective row.
def isOnlyinRow(puz_no, poss_coord):
    for coord in poss_dict[puz_no]:
        if coord != poss_coord and coord[0] == poss_coord[0] or isAnyConflict(puz_no, poss_coord):
            return False
        else: continue
    return True

# Define function that deterrmines if a possible coordinate for a given number is the only possible coordinate in its respective column.
def isOnlyinCol(puz_no, poss_coord):
    for coord in poss_dict[puz_no]:
        if coord != poss_coord and coord[1] == poss_coord[1] or isAnyConflict(puz_no, poss_coord):
            return False
        else: continue
    return True

# Define function that determines if a possible coordinate for a given number is the only possible coordinate it its respective 3x3 box
def isOnlyinBox(puz_no, poss_coord):
    for box in boxes:
        if poss_coord in box:
            for coord in poss_dict[puz_no]:
                if coord != poss_coord and coord in box or isAnyConflict(puz_no, poss_coord):
                    return False
                else: continue
    return True

# Declare and initialize dictionary that only retains newly solved numbers
newNum_dict = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}

# Declare variable that counts how many coordinates will have been eliminated from possibilities by following function
new_elims = 0

# Define function that combines "isOnly" functions into a single function that loops through all possibilities,
# determines if there are any solutions, and updates the relevant data structure if (a) solution(s) is/are found
def onlyOnes():
    global amt_solved, new_elims

    for p_no in poss_dict:
        for pd_coord in poss_dict[p_no]:
            if isOnlyinRow(p_no, pd_coord) or isOnlyinCol(p_no, pd_coord) or isOnlyinBox(p_no, pd_coord):
                num_dict[p_no].append(pd_coord)
                puzzle_list[pd_coord[0]][pd_coord[1]] = p_no
                newNum_dict[p_no].append(pd_coord)
                solved_coords.append(pd_coord)
                solver_solved[p_no].append(pd_coord)
                amt_solved += 1
                new_elims += 1
            else: continue
        for new_num in newNum_dict:
            for new_coord in newNum_dict[new_num]:
                for pnum in poss_dict:
                    for pcoord in poss_dict[pnum]:
                        if new_coord in poss_dict[pnum]:
                            poss_dict[pnum].remove(new_coord)
                            if isGuess:
                                guessDependElim[-1].append((pnum, new_coord))
                        else: continue

# Define function that eliminates possibilities if there is a conflict with solved numbers
def directConflictElim():
    global new_elims

    for num in poss_dict:
        np_cds = []
        for po_cd in poss_dict[num]:
            if isAnyConflict(num, po_cd):
                np_cds.append(po_cd)
        for np_cd in np_cds:
            poss_dict[num].remove(np_cd)
            if isGuess:
                guessDependElim[-1].append((num, np_cd))
            new_elims += 1


# >> Iterative Guessing Algorithms ----------------------------------------------------------------------------------

# The functions and variables below are used if the puzzle can't be solved via the previous methods
# and guesses must be taken and iterated on to find the values that complete the puzzle

# Keep list of coordinate sets that have been guessed from to try to solve puzzle
guessSets = []

# Keep a list of how many times each set of guess possibilities has been iterated on
guessAmt = []

# Keep track of set sizes
guessSetSize = []

# Keep a list of (lists of) coordinates eliminated while dependent on a guess
guessDependElim = []

# Declare boolean that indicates whether there are any guessed values
isGuess = False

# Declare boolean that indicates whether a guess set has been exhausted, which causes the program 
# to revisit the set before it and iterate, assuming a wrong guess was further back in the chain of 
# guesses than the set whose possibilities were just exhausted before the program could complete
setExhausted = False

# Define function that selects a number and set of coordinates to use as guesses in the puzzle
def newGuessSet():
    global amt_solved, new_elims
    num_poss_list = []
    guess_options = []
    
    # Make list of numbers that still need to be solved and how many potential coordinates
    # there are for each number
    for num in poss_dict:
        if len(poss_dict[num]) > 1:
            num_poss_list.append((len(poss_dict[num]), num))
        else: continue
                
    # Use the number with the minimum number of possibilites to increase chances of guessing correctly
    try_num = min(num_poss_list)[1]

    # Find the element (3x3 box, row, column) that contains the least number of possibilities from which to take a guess
    for trycrd in poss_dict[try_num]:
            
        # Check which boxes have multiple possibilities
        for box in range(len(boxes)):
            if trycrd in boxes[box]:
                box_crds = [trycrd]
                for otherboxcrd in poss_dict[try_num]:
                    if otherboxcrd != trycrd and otherboxcrd in boxes[box] and otherboxcrd not in box_crds:
                        box_crds.append(otherboxcrd)
                if len(box_crds) > 1:
                    guess_options.append((len(box_crds), box_crds))
                    
        # Check which rows have multiple possibilities
        for row in range(len(puzzle_list)):
            if row == trycrd[0]:
                row_crds = [trycrd]
                for otherrowcrd in poss_dict[try_num]:
                    if otherrowcrd != trycrd and otherrowcrd[0] == row and otherrowcrd not in row_crds:
                        row_crds.append(otherrowcrd)
                if len(row_crds) > 1:
                    guess_options.append((len(row_crds), row_crds))
                    
        # Check which columns have multiple possibilities
        for col in range(len(puzzle_list)):
            if col == trycrd[1]:
                col_crds = [trycrd]
                for othercolcrd in poss_dict[try_num]:
                    if othercolcrd != trycrd and othercolcrd[1] == col and othercolcrd not in col_crds:
                        col_crds.append(othercolcrd)
                if len(col_crds) > 1:
                    guess_options.append((len(col_crds), col_crds))

    guess_elmnt = (try_num, min(guess_options)[1])
    
    # Find the row, box, or column from which to take a guess based on least number of possibilities
    guessAmt.append(1)
    guessSetSize.append(len(guess_elmnt[1]))
    guessSets.append(guess_elmnt)
    guessDependElim.append([])
    for elcrd in guess_elmnt[1]:
        if elcrd in poss_dict[try_num]:
            poss_dict[try_num].remove(elcrd)
            guessDependElim[-1].append((try_num, elcrd))
        else: continue
    num_dict[try_num].append(guess_elmnt[1][0])
    puzzle_list[guess_elmnt[1][0][0]][guess_elmnt[1][0][1]] = try_num
    solved_coords.append(guess_elmnt[1][0])
    newNum_dict[try_num].append(guess_elmnt[1][0])
    new_elims += len(guess_elmnt[1])
    amt_solved += 1


# Define function that determines how to take a guess if it's needed to solve the puzzle
def guessIt():
    global amt_solved, new_elims, isGuess, setExhausted

    isGuess = True
    poss_count = 0
    for no in poss_dict:
        poss_count += len(poss_dict[no])

    # If the puzzle remains unsolved because no solution could be isolated from possibilities:
    if len(solved_coords) < 81 and poss_count > 1 and not setExhausted:
        newGuessSet()
        
    # If the solver 'locked up' because a previous guess (in potentially a chain of guesses)
    # was incorrect:
    elif len(solved_coords) < 81 and poss_count == 0 or setExhausted:

        # If all possibilities from a set of guesses haven't been tried:
        if guessAmt[-1] < len(guessSets[-1][1]):
            setExhausted = False
            
            # Re-add coordinates removed from pool of possibilities based on last guess to pool
            # and remove numbers solved in puzzle based on last guess from puzzle
            for guesstup in guessDependElim[-1]:
                for pnum in poss_dict:
                    if guesstup[0] == pnum and guesstup[1] not in poss_dict[pnum]:
                        poss_dict[pnum].append(guesstup[1])
                for num in num_dict:
                    if puzzle_list[guesstup[1][0]][guesstup[1][1]] == num:
                        num_dict[num].remove(guesstup[1])
                        solved_coords.remove(guesstup[1])
                        amt_solved -= 1
                puzzle_list[guesstup[1][0]][guesstup[1][1]] = 0
                
            # Select next coordinate from the guess set and use that as guess
            guessAmt[-1] += 1
            num_dict[guessSets[-1][0]].append(guessSets[-1][1][guessAmt[-1]-1])
            amt_solved += 1
            for setcrd in guessSets[-1][1]:
                if setcrd in poss_dict[guessSets[-1][0]]:
                    poss_dict[guessSets[-1][0]].remove(setcrd)
                    guessDependElim[-1].append((guessSets[-1][0], setcrd))
            puzzle_list[guessSets[-1][1][guessAmt[-1]-1][0]][guessSets[-1][1][guessAmt[-1]-1][1]] = guessSets[-1][0]
            solved_coords.append(guessSets[-1][1][guessAmt[-1]-1])
            newNum_dict[guessSets[-1][0]].append(guessSets[-1][1][guessAmt[-1]-1])
            new_elims += len(guessSets[-1][1])
                

        # If all possibilities from a set of guesses have been tried and the puzzle 'locks up',
        # it means a previous guess in the chain was wrong, since one coordinate in the set
        # had to be the correct one.  The last set must be deleted and the previous one revisited
        else:
            setExhausted = True
            #print("Guess Sub-Condition: guess set exhausted")
            # First, add possibilites removed from that set back to possible coordinates
            # and remove values from the puzzle that were based on that set of guesses
            for guesstup in guessDependElim[-1]:
                for pnum in poss_dict:
                    if guesstup[0] == pnum and guesstup[1] not in poss_dict[pnum]:
                        poss_dict[pnum].append(guesstup[1])
                for num in num_dict:
                    if puzzle_list[guesstup[1][0]][guesstup[1][1]] == num:
                        num_dict[num].remove(guesstup[1])
                        solved_coords.remove(guesstup[1])
                        amt_solved -= 1
                puzzle_list[guesstup[1][0]][guesstup[1][1]] = 0
                
            # Next, remove the entire previous set of guesses, so the set before it can be
            # revisited the next time the loop goes around
            guessAmt.pop(-1)
            guessSetSize.pop(-1)
            guessSets.pop(-1)
            guessDependElim.pop(-1)
            new_elims = 1

    # If puzzle is finished, solve any remaining value and exit solver loop
    else:
        onlyOnes()
        new_elims = 0
        
            
# >> SOLVER START AND LOOP SECTION ===================================================================================

# Import the time module to time the solver
import time

# Record time at start of solve
start_time = time.time()

# Start solve by immediately eliminating coordinates as possibilities that conflict with
# starting numbers by row, column, and 3x3 box
for num in poss_dict:
    for r in range(len(puzzle_list)):
        for c in range(len(puzzle_list[r])):
            if not isAnyConflict(num, (r, c)):
                    poss_dict[num].append((r, c))
    
# Loop through, updating puzzle and other relevant data structures until no new coordinates are eliminated
# (indicates that puzzle is either solved, unsolvable, or not solvable via currently included methods)       
x = 0
while x < 1 or new_elims > 0 and x < 3500:
    new_elims = 0
    newNum_dict = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
    onlyOnes()
    directConflictElim()
    if new_elims == 0:
        onlyOnes()
        guessIt()
    x += 1


# Record time when puzzle finishes solving and find duration by subtracting start time
end_time = time.time()
duration = end_time - start_time

# Print solved puzzle and the time it took to find a solution
print('\nThe puzzle solved ' + str(amt_solved) + ' values and ' + f'{((amt_solved/(81-start_amt))*100):.0f}% of the open squares in\n'
      + f'{duration:.3f} seconds and ' + str(x) + ' iterations.')

# Print out the results in a visually comprehensible manner
print_puzzle(puzzle_list)

# %%