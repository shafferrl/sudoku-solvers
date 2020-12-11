"""
Sudoku solver that runs as a desktop program using the
Python GUI library, Tkinter.

Certain windows were sized statically on Windows 10
and may not display with the proper dimensions on
other operating systems.  Other styling may not display
as intended on other systems.

====================== Version 2 Updates ========================
=>  Changed some smaller for loops used to populate lists
    to list comprehension syntax.
=>  Improved some GUI-related quirks.
=>  Added unique window icon.
=>  Changed program_name variable to derive from python module name.

"""

# Relevant library imports
from tkinter import *
from tkinter import ttk, messagebox
import webbrowser, sys

# Assign program name to variable, so any reference to it is tied to one
# line of code should program name be changed
program_name = (''.join(sys.argv[0].split('\\')[-1]).split('/')[-1]).split('.')[0]
print(sys.argv)
#program_name = sys.modules['__main__'].__file__.split('/')[-1].split('\\')[-1].split('.')[0]

# Generate, size, and style main GUI window for program
root = Tk()
about = None
root.title(program_name)
root.minsize(445, 505)
root.maxsize(445, 505)
#root.iconbitmap("C:/Users/shaff/Desktop/Python Scripts/SudokuPicture.ico")
img = Image("photo", file="../images/SudokuPicture.png")
root.tk.call('wm','iconphoto', root._w, img)
styleA = ttk.Style()
styleA.configure("P1.P2.TButton", background="gray85", font=("Helvetica", 20), foreground="blue")
style1 = ttk.Style()
style1.configure("TFrame", background="gray55")
style1.configure("P2.TButton", background="gray85", font=("Helvetica", 20), foreground="gray25")
style2 = ttk.Style()
style2.configure("B.TButton", background="gray85", font=("", 10))
style_link = ttk.Style()

# Declare and initialize boolean variables that control puzzle clearing and example loading
# functions and provide safeguard against accidentally deleting entered/solved values
clearbool = False
loadbool = False

# Define function that clears and re-initializes all values in the puzzle
def clearpuzzle():
    global loadbool, clearbool, amt_solved, numberofentries, num_dict, numbers, solver_solved, newNum_dict, solved_coords, new_elims, guessSets, guessAmt, guessDependElim, isGuess, setExhausted, poss_dict, puzzle_list
    if numberofentries > 0:
        clear = messagebox.askyesno("New Puzzle","Are you sure you want to proceed?")
        if clear:
            clearbool = True
            num_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
            poss_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
            solver_solved = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
            newNum_dict = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
            puzzle_list = [[0 for c in range(9)] for r in range(9)]
            new_elims = 0
            amt_solved = 0
            guessSets = []
            guessAmt = []
            guessDependElim = []
            solved_coords = []
            isGuess = False
            setExhausted = False
            convert_backtofront()
            for n in numbers:
                n[0].set(0)
                n[1].set('')
            numberofentries = 0
        else: clearbool = False
    else: pass

# Define function that clears only values from the puzzle that the solver has generated. User-entered values will be retained
def clearsolved():
    global amt_solved, numberofentries, num_dict, numbers, solver_solved, newNum_dict, solved_coords, new_elims, guessSets, guessAmt, guessDependElim, isGuess, setExhausted, poss_dict, puzzle_list
    if amt_solved > 0:
        clearsolved = messagebox.askyesno("Clear Solved Values","Are you sure you want to proceed?")
        if clearsolved:
            for num in solver_solved:
                for crd in solver_solved[num]:
                    puzzle_list[crd[0]][crd[1]] = 0
                    absindx = crd[1]%3 + 3*(crd[0]%3) + 9*(int(crd[1]/3)) + 27*(int(crd[0]/3))
                    numbers[absindx][0].set(0)
                    numbers[absindx][1].set('')
                    num_dict[num].remove(crd)
                    solved_coords.remove(crd)
                    numberofentries -= 1
            isGuess = False
            setExhausted = False
            new_elims = 0
            amt_solved = 0
            guessSets = []
            guessAmt = []
            guessDependElim = []
            poss_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
            solver_solved = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
            convert_backtofront()
        else: pass
    else: pass

# Define function that links to external resource referenced in Help menu
def linkMIT(*args):
    webbrowser.open("https://www.technologyreview.com/s/426554/mathematicians-solve-minimum-sudoku-problem/")

# Define function that links to external resource referenced in Help menu
def linkTelegraph(*args):
    webbrowser.open("https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html")

# Define function that generates "About" window and content available in Help menu
def About():

    global about
    about = Tk()
    about.title("About " + program_name)

    about.minsize(445, 505)
    about.maxsize(445, 505)

    about_text1 = "Welcome to "+program_name+"!\n\nThis program will solve Sudoku puzzles when you enter the values into the puzzle. "\
    "Click on each puzzle square and select the appropriate number for the puzzle you are trying to crack.  Be aware that as you click on "\
    "the buttons, they will skip past conflicting numbers to the next possible value.\n\n"\
    "When you are satisfied with the numbers you have entered into the puzzle, hit the \"Solve Puzzle\" button "\
    "to solve the puzzle.  To start a new puzzle, select \"Clear Puzzle\" from the File menu, and the values will be cleared.  You can "\
    "also clear only the solved values by selecting \"Clear Solved Vaues\" in the File menu.\n\n"\
    "There are some example puzzles in the File menu, so you can see the solver work before entering a puzzle yourself if you like.\n\n"\
    "This program will attempt to solve any puzzle with more than 16 numbers entered, so be diligent about what you enter into the puzzle.  "\
    "If you enter a set of 17 or more numbers that has more than one solution, the program will just present the first solution it finds.  "\
    "Most puzzles will solve in a fraction of a second, but the hardest ones can take on the order of minutes in some cases."
    about_textA = Label(about, text=about_text1,  wraplength=422, justify=LEFT)
    about_textA.grid(row=0, padx=12, pady=5, column=0)
    
    linkMITtext = "\"Mathematicians Solve Minimum Sudoku Problem\""
    MITlink = Label(about, text=linkMITtext,  wraplength=422, justify=LEFT, fg="blue", cursor="hand2", font=("calibri", 10, "underline"))
    MITlink.grid(row=1, column=0, padx=12, pady=2)
    MITlink.bind("<Button-1>", linkMIT)
    
    about_text2 = "While the program will attempt to solve anything with more than 17 entries, keep in mind that every open square introduces exponentially "\
                  "more possibilites.  The number of iterations the program will run before stopping is currently capped to a little less than twice that "\
                  "needed to solve the \"World's Hardest Sudoku\" in the Example menu.  Future versions of this program may introduce more sophisticated "\
                  "algorithms to reduce solve time, remove the iteration cap, and determine if there are multiple solutions for a set of inputs."
    about_textB = Label(about, text=about_text2,  wraplength=422, justify=LEFT)
    about_textB.grid(row=2, column=0, padx=12, pady=5)

    linkHardestSudokutext = "\"The World's Hardest Sudoku:  Can You Crack it?\""
    hardestSudokuLink = Label(about, text=linkHardestSudokutext, wraplength=422, justify=LEFT, fg="blue", cursor="hand2", font=("calibri", 10, "underline"))
    hardestSudokuLink.grid(row=3, column=0, padx=12, pady=2)
    hardestSudokuLink.bind("<Button-1>", linkTelegraph)

    
# Define function that takes the information from data structures used by the solver and
# transfers the information to data structures used to generate puzzle GUI
def convert_backtofront():
    global numberofentries
    numberofentries = 0
    for num in num_dict:
        for crd in num_dict[num]:
            puzzle_list[crd[0]][crd[1]] = num
            absindx = crd[1]%3 + 3*(crd[0]%3) + 9*(int(crd[1]/3)) + 27*(int(crd[0]/3))
            numbers[absindx][0].set(num)
            numbers[absindx][1].set(str(num))
            numberofentries += 1
            if crd in solver_solved[num]:
                buttons[absindx] = ttk.Button(buttonrowframes[int(absindx/3)], style="P1.P2.TButton", width=2, textvariable=numbers[absindx][1],
                                                  command = lambda n= numbers[absindx][0], s= numbers[absindx][1]: numinc(n,s))
            elif crd not in solver_solved[num]:
                buttons[absindx] = ttk.Button(buttonrowframes[int(absindx/3)], style="P2.TButton", width=2, textvariable=numbers[absindx][1],
                                                  command = lambda n= numbers[absindx][0], s= numbers[absindx][1]: numinc(n,s))
                
# Take user-entered data and transfer it into data structures more useful to solver
def convert_fronttoback():
    for absi in range(len(numbers)):
        if numbers[absi][0].get() != 0:
            row = 3*int(absi/27)+int(int(absi%9)/3)
            col = (int(absi/9)*3 + int(absi%3)) - 9*int(absi/27)
            if (row, col) not in num_dict[numbers[absi][0].get()]:
                num_dict[numbers[absi][0].get()].append((row, col))

# Define function that loads an example puzzle available in drop-down menu 
def loadexample(exno):
    global clearbool, num_dict, numbers, loadbool, numberofentries
    clearpuzzle()
    if clearbool or numberofentries == 0:
        if exno == 9:
            sure = messagebox.askokcancel("\"World's Hardest Sudoku\"","This one will take a few minutes to solve.")
        if exno != 9 or sure:
            clearbool = False
            for ni in range(len(numbers)):
                    buttons[ni] = ttk.Button(buttonrowframes[int(ni/3)], style="P2.TButton", width=2, textvariable=numbers[ni][1],
                                             command = lambda n= numbers[ni][0], s= numbers[ni][1]: numinc(n,s))
            for num in exampletuple[exno]:
                for excrd in exampletuple[exno][num]:
                    num_dict[num].append(excrd)
            for no in num_dict:
                for scrd in num_dict[no]:
                    solved_coords.append(scrd)
            convert_backtofront()
        else: pass
    else: pass

# Define function that exits from program upon selecting command and closes all windows
def Exit():
    exitprogram = messagebox.askyesno("Exit "+program_name, "Are you sure you want to exit "+program_name+"?")
    if exitprogram:
        root.destroy()
        try: about.destroy()
        except: pass
        root.quit()
    else: pass

root.protocol('WM_DELETE_WINDOW', Exit)

# Generate and configure drop-down menus
root.option_add('*tearOff', FALSE)
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
examplemenu = Menu(filemenu)

filemenu.add_command(label="Clear Puzzle", command=clearpuzzle)
filemenu.add_command(label="Clear Solved Values", command=clearsolved)
filemenu.add_cascade(label="Examples\t\t\t", menu=examplemenu)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=Exit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

examplemenu.add_command(label="Puzzle 1       Easy", command= lambda x=0: loadexample(x))
examplemenu.add_separator()
examplemenu.add_command(label="Puzzle 2       Medium", command= lambda x=1: loadexample(x))
examplemenu.add_command(label="Puzzle 3", command = lambda x=2: loadexample(x))
examplemenu.add_command(label="Puzzle 4", command= lambda x=3: loadexample(x))
examplemenu.add_separator()
examplemenu.add_command(label="Puzzle 5       Med/Hard", command= lambda x=4: loadexample(x))
examplemenu.add_command(label="Puzzle 6", command= lambda x=5: loadexample(x))
examplemenu.add_separator()
examplemenu.add_command(label="Puzzle 7       Hard", command= lambda x=6: loadexample(x))
examplemenu.add_command(label="Puzzle 8 ", command= lambda x=7: loadexample(x))
examplemenu.add_command(label="Puzzle 9", command= lambda x=8: loadexample(x))
examplemenu.add_separator()
examplemenu.add_command(label="\"World's Hardest Sudoku\"", command= lambda x=9: loadexample(x))


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

# Consolidate input conflict-type functions into single function
def isInputConflict(puz_number, coord_tuple):
    
    #Check to see if there is already a number at the index entered
    if puzzle_list[coord_tuple[0]][coord_tuple[1]] != 0:
        return 1
    
    #Check columns and rows
    if isRowConflict(puz_number, coord_tuple) or isColConflict(puz_number, coord_tuple):
        return 2
    #Check 3x3 boxes
    if isBoxConflict(puz_number, coord_tuple):
        return 3
    return 0

# Resolve any input conflict into single yes/no rather than distinguishing by type.
# This will be cleaner in instances where the type of conflict need not be known
def isAnyConflict(puz_number2, coord_tuple2):
    
    if isInputConflict(puz_number2, coord_tuple2) == 1:
        return True
    if isInputConflict(puz_number2, coord_tuple2) == 2:
        return True
    elif isInputConflict(puz_number2, coord_tuple2) == 3:
        return True
    return False

# Define function that increments the numbers associated with the button-squares in the GUI
# when a button-square is clicked and skips over values that would cause conflict
def numinc(index, val, valstr):
    global numberofentries
    numberofentries = 0
    acceptable_val = False
    row = 3*int(index/27)+int(int(index%9)/3)
    col = (int(index/9)*3 + int(index%3)) - 9*int(index/27)
    inc_tup = (row, col)
    if val.get() != 0:
        num_dict[val.get()].remove(inc_tup)
        puzzle_list[row][col] = 0
        if numberofentries != 0: numberofentries -= 1
    while not acceptable_val:
        val.set((val.get()+1)%10)
        if val.get() != 0:
            if isAnyConflict(val.get(), inc_tup):
                continue
            else:
                num_dict[val.get()].append(inc_tup)
                puzzle_list[row][col] = val.get()
                acceptable_val = True
        else: acceptable_val = True
    if val.get() == 0:
        valstr.set('')
    else: valstr.set(str(val.get()))
    for n in numbers:
        if n[0].get() != 0: numberofentries +=1

# Declare and initalize lists that will be used to generate button-square matrix
numbers = []
boxrowframes = []
boxcolframes = []
buttonrowframes = []
buttons = []

# Variable that keeps tally of numbers entered
numberofentries = 0

# Define function that generates button-square matrix in GUI and associates
# each button with incrementing function
def renderpuzzle():
    
    outer_frame = ttk.Frame(root, borderwidth=0, style="TFrame")
    outer_frame.pack(side="top", fill="both", expand=True, padx=12, pady=12)
    
    inc = 3

    for i in range(3):
        boxrowframes.append(ttk.Frame(outer_frame, style="TFrame"))
        boxrowframes[i].pack(side="top", fill="both", expand=True)
        for j in range(3):
            boxcolframes.append(ttk.Frame(boxrowframes[i], borderwidth=1, style="TFrame"))
            boxcolframes[i*inc+j].pack(side="left", fill="both", expand=True)
            for k in range(3):
                buttonrowframes.append(ttk.Frame(boxcolframes[i*inc+j], style="TFrame"))
                buttonrowframes[(i*inc+j)*inc+k].pack(side="top", fill="both", expand=True)
                for el in range(3):
                    numbers.append((IntVar(), StringVar()))    
                    buttons.append(ttk.Button(buttonrowframes[(i*inc+j)*inc+k], style="P2.TButton", width=2, textvariable=numbers[(i*inc**2+j*inc+k)*inc+el][1],
                                              command = lambda x=(i*inc**2+j*inc+k)*inc+el, n= numbers[(i*inc**2+j*inc+k)*inc+el][0], s= numbers[(i*inc**2+j*inc+k)*inc+el][1]: numinc(x,n,s)))
                    buttons[(i*inc**2+j*inc+k)*inc+el].pack(side="left", fill="both", expand=True)

renderpuzzle()

# Declare and initialize primary data structures used by solver algorithm
num_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
puzzle_list = [[0 for c in range(9)] for r in range(9)]

# Declare the data structures and functions that will be referenced and updated when the puzzle is solving

# Declare dictionary of possible coordinates of each number.  Will be populated with input coordinates after
# functions are defined to preclude function definitions from being included in puzzle solution timer

poss_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}

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
isGuess = False

# Declare boolean that indicates whether a guess set has been exhausted, which causes the program 
# to revisit the set before it and iterate, assuming a wrong guess was further back in the chain of 
# guesses than the set whose possibilities were just exhausted before the program could complete
setExhausted = False

# Define function that determines if a possible coordinate for a given number is the only possible coordinate in its respective row
def isOnlyinRow(puz_no, poss_coord):
    for coord in poss_dict[puz_no]:
        if coord != poss_coord and coord[0] == poss_coord[0] or isAnyConflict(puz_no, poss_coord):
            return False
        else: continue
    return True

# Define function that deterrmines if a possible coordinate for a given number is the only possible coordinate in its respective column
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
            
# Define function that selects a number and set of coordinates to use as guesses in the puzzle
def newGuessSet():
    global amt_solved
    global new_elims
    num_poss_list = []
    guess_options = []
    # Make list of numbers that still need to be solved and how many potential coordinates there are for each number
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
    guessSets.append(guess_elmnt)
    guessDependElim.append([])
    for elcrd in guess_elmnt[1]:
        if elcrd in poss_dict[try_num]:
            poss_dict[try_num].remove(elcrd)
            guessDependElim[-1].append((try_num, elcrd))
        else: continue
    num_dict[try_num].append(guess_elmnt[1][0])
    solver_solved[try_num].append(guess_elmnt[1][0])
    puzzle_list[guess_elmnt[1][0][0]][guess_elmnt[1][0][1]] = try_num
    solved_coords.append(guess_elmnt[1][0])
    newNum_dict[try_num].append(guess_elmnt[1][0])
    new_elims += len(guess_elmnt[1])
    amt_solved += 1

# Define function that determines how to take a guess if it's needed to solve the puzzle
def guessIt():
    global amt_solved, new_elims, isGuess, setExhausted

    isGuess = True
    poss_count = sum(len(poss_dict[no]) for no in poss_dict)
    '''
    for no in poss_dict:
        poss_count += len(poss_dict[no])'''

    # If the puzzle remains unsolved because no solution could be isolated from possibilities
    if len(solved_coords) < 81 and poss_count > 1 and not setExhausted:
        newGuessSet()
    # If the solver 'locked up' because a previous guess (in potentially a chain of guesses) was incorrect
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
                        solver_solved[num].remove(guesstup[1])
                        solved_coords.remove(guesstup[1])
                        amt_solved -= 1
                puzzle_list[guesstup[1][0]][guesstup[1][1]] = 0
            # Select next coordinate from the guess set and use that as guess
            guessAmt[-1] += 1
            num_dict[guessSets[-1][0]].append(guessSets[-1][1][guessAmt[-1]-1])
            solver_solved[guessSets[-1][0]].append(guessSets[-1][1][guessAmt[-1]-1])
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
            # First, add possibilites removed from that set back to possible coordinates
            # and remove values from the puzzle that were based on that set of guesses
            for guesstup in guessDependElim[-1]:
                for pnum in poss_dict:
                    if guesstup[0] == pnum and guesstup[1] not in poss_dict[pnum]:
                        poss_dict[pnum].append(guesstup[1])
                for num in num_dict:
                    if puzzle_list[guesstup[1][0]][guesstup[1][1]] == num:
                        num_dict[num].remove(guesstup[1])
                        solver_solved[num].remove(guesstup[1])
                        solved_coords.remove(guesstup[1])
                        amt_solved -= 1
                puzzle_list[guesstup[1][0]][guesstup[1][1]] = 0
                
            # Next, remove the entire previous set of guesses, so the set before it can be
            # revisited the next time the loop goes around
            guessAmt.pop(-1)
            guessSets.pop(-1)
            guessDependElim.pop(-1)
            new_elims = 1

    # If puzzle is finished, solve any remaining value and exit solver loop.
    else:
        onlyOnes()
        new_elims = 0

# Define function that runs loop calling solver functions.  Function provides
# error message if user has entered too few values into puzzle
def attemptsolve():
    global numberofentries, num_dict, amt_solved, solver_solved, newNum_dict, new_elims, guessSets, guessAmt, guessDependElim, isGuess, setExhausted, poss_dict
    
    if numberofentries < 17:
        errmessage = messagebox.showerror("Not Enough Information", "There must be at least 17 entries for a unique solution.\n"\
                                          "See Help menu for more information.")
    else:
        if numberofentries < 21:
            solvelots = messagebox.askokcancel("Minimal Input", "This might take awhile.  Are you sure you want to proceed?\n"\
                                               "See Help menu for more information.")

        if numberofentries >= 21 or solvelots:
            # Keep list of coordinates for which the number in that coordinate is solved
            for num in num_dict:
                for scrd in num_dict[num]:
                    if scrd not in solved_coords:
                        solved_coords.append(scrd)

            start_amt = len(solved_coords)
                
            # Start solve by immediately eliminating coordinates as possibilities that conflict with
            # starting numbers by row, column, and 3 x 3 box
            for num in poss_dict:
                for r in range(len(puzzle_list)):
                    for c in range(len(puzzle_list[r])):
                        if not isAnyConflict(num, (r, c)):
                                poss_dict[num].append((r, c))
            # Loop through, updating puzzle and other relevant data structures until no new coordinates are eliminated
            # (Indicates that puzzle is either solved, unsolvable, or not solvable via currently included methods)      
            its = 0
            while its < 1 or new_elims > 0 and its < 5000:
                new_elims = 0
                newNum_dict = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
                onlyOnes()
                directConflictElim()
                if new_elims == 0:
                    onlyOnes
                    guessIt()
                its += 1
            onlyOnes()      
            convert_backtofront()

        else: pass

# Define function that generates "Solve Puzzle" button
def rendersolvebutton():
    solve_frame = ttk.Frame(root, style="TFrame")
    solve_frame.pack(side="top", expand=False, pady=18)
    solve_button = ttk.Button(solve_frame, text="Solve Puzzle", width=18, style="B.TButton", command=attemptsolve)
    solve_button.pack(side="top", fill="both", expand=True, padx=1, pady=1)

# Generate "Solve Puzzle" button.
rendersolvebutton()

# Declare data structure containing all example puzzles selectable in drop-down menu
exampletuple = ({1:((2,8),(6,6),(7,4)),2:((0,5),(3,0),(7,2),(8,4)),3:((0,4),(8,6),(5,8),(4,5)),4:((0,2),(1,4),(4,0),(7,1),(5,5)),5:((3,3),(4,1),(1,7)),6:((2,2),(4,3)),7:((4,8),),8:((1,6),(4,7),(8,2)),9:((0,6),(6,0),(8,3))},
                {1:((1,8),(4,6),(6,7),(7,1),(8,4)),2:((4,4),(7,0)),3:((0,7),(2,4),(3,0),(6,5)),4:((1,4),(4,2),(5,8),(7,6),(8,1)),5:((0,8),(2,1),(6,4)),6:((1,7),(4,1),(5,4),(8,0)),7:((1,2),(2,6),(4,7),(7,4)),8:((2,3),(3,4),(6,2),(7,8)),9:((1,0),(0,4))},
                {1:((2,6),(4,7),(5,4)),2:((1,0),(2,5),(4,1),(3,4)),3:((4,6),(6,3),(8,7)),4:((0,5),(7,4)),5:((2,1),(5,2),(4,4),(6,7)),6:((2,4),(1,8),(7,0),(8,3)),7:((3,5),(6,2)),8:((0,1),(1,4)),9:((3,6),(4,2),(5,3),(6,4),(7,8))},
                {1:((0,0),(4,6),(7,8)),2:((1,2),(5,1)),3:((1,3),(3,7),(7,5)),4:((0,5),(3,3),(2,7),(7,6),(8,4)),5:((0,4),(1,6)),6:((4,2),(6,1),(8,3)),7:((1,0),(2,6),(5,5),(7,2),(8,8)),8:((3,0),(1,5),(5,8)),9:((6,2),(7,3))},
                {1:((8,4),),2:((1,1),(5,0),(4,3),(7,4)),3:((0,4),(4,1),(5,8),(8,2),(7,7)),4:((2,7),(3,0),(4,5),(6,4)),5:((0,0),(2,4),(3,8),(5,5),(6,1),(8,3)),6:((2,2),(0,6),(8,7)),7:((0,5),(4,7),(6,6)),8:((0,1),(1,4),(3,3),(8,8)),9:()},
                {1:((0,3),(2,1),(5,4)),2:((1,7),(3,1),(8,4),(7,8)),3:((0,0),(1,4),(5,5),(8,7)),4:((3,6),(5,3),(7,4),(8,8)),5:((0,5),(8,3)),6:((0,1),(3,4),(8,5)),7:((3,3),(5,7),(7,1)),8:((0,4),(5,2),(6,7)),9:((1,0),(3,5))},
                {1:((1,0),(5,2),(3,6),(4,5)),2:((4,0),(3,4),(1,2),(8,5)),3:((0,0),(4,3),(3,8)),4:((5,0),(6,3),(7,6),(2,4)),5:((0,3),(6,6),(4,8)),6:((2,5),(5,4),(8,7)),7:((2,2),(8,8)),8:((6,4),),9:((0,1),(7,8))},
                {1:((5,0),(2,1),(3,7),(8,6)),2:((0,4),(2,0),(6,8),(8,3)),3:((0,0),(3,2),(7,6)),4:((0,2),(3,8),(6,6)),5:((8,4),),6:((5,1),(4,5)),7:((1,2),(2,3),(6,7)),8:((2,2),(0,5),(8,8)),9:((4,3),(5,6),(6,5))},
                {1:((0,0),(2,6),(3,4)),2:((5,6),(8,3)),3:((1,8),(4,5),(7,4),(8,0)),4:((3,2),(5,4),(6,8),(7,0)),5:((0,8),(6,3),(8,2)),6:((0,6),(1,4)),7:((3,1),(4,3)),8:((2,5),(5,7),(8,8)),9:((2,0),(0,5),(6,2))},
                {1:((5,3),(7,7),(6,2)),2:((2,6),),3:((1,2),(5,7)),4:((4,4),(8,6)),5:((4,5),(7,3),(3,1)),6:((1,3),(6,7)),7:((2,1),(3,5),(4,6)),8:((0,0),(6,8),(7,2)),9:((2,4),(8,1))})

root.mainloop()
