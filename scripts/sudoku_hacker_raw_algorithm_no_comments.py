""" Heavily commented code with comments deleted and blank lines removed to see code line count."""
class SudokuSolver:
    numberofentries = 0
    num_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
    puzzle_list = [[0 for c in range(9)] for r in range(9)]
    poss_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
    solved_coords = []
    solver_solved = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
    amt_solved = 0
    newNum_dict = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
    new_elims = 0
    guessSets = []
    guessAmt = []
    guessDependElim = []
    is_guess = False
    setExhausted = False
    def __init__(self, form_data):
        self.numbers = form_data
        self.convert_fronttoback()
        self.check_initial_conflict()
    def check_initial_conflict(self):
        for no in self.num_dict:
            for coord in self.num_dict[no]:
                if self.isOnlyinRow(no, coord, self.num_dict) or self.isOnlyinCol(no, coord, self.num_dict) or self.isOnlyinBox(no, coord, self.num_dict):
                    pass
                else:
                    print(no, ' ', coord)
                    raise ValueError('Puzzle Input Conflict')
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
    def convert_fronttoback(self):
        for cell in self.numbers:
            if self.numbers.get(cell):
                self.num_dict[int(self.numbers[cell])].append((int(cell[-2]), int(cell[-1])))
                self.numberofentries += 1
        for num in self.num_dict:
            for num_crd in self.num_dict[num]:
                self.puzzle_list[num_crd[0]][num_crd[1]] = num
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
    def isInputConflict(self, puz_number, coord_tuple):
        if self.puzzle_list[coord_tuple[0]][coord_tuple[1]] != 0:
            return 1
        if self.isRowConflict(puz_number, coord_tuple) or self.isColConflict(puz_number, coord_tuple):
            return 2
        if self.isBoxConflict(puz_number, coord_tuple):
            return 3
        return 0
    def isAnyConflict(self, puz_number2, coord_tuple2):
        if self.isInputConflict(puz_number2, coord_tuple2) == 1:
            return True
        if self.isInputConflict(puz_number2, coord_tuple2) == 2:
            return True
        elif self.isInputConflict(puz_number2, coord_tuple2) == 3:
            return True
        return False
    def isOnlyinRow(self, puz_no, poss_coord, check_dict):
        for coord in check_dict[puz_no]:
            if coord != poss_coord and coord[0] == poss_coord[0] or self.isAnyConflict(puz_no, poss_coord) and check_dict is not self.num_dict:
                return False
            else: continue
        return True
    def isOnlyinCol(self, puz_no, poss_coord, check_dict):
        for coord in check_dict[puz_no]:
            if coord != poss_coord and coord[1] == poss_coord[1] or self.isAnyConflict(puz_no, poss_coord) and check_dict is not self.num_dict:
                return False
            else: continue
        return True
    def isOnlyinBox(self, puz_no, poss_coord, check_dict):
        for box in self.boxes:
            if poss_coord in box:
                for coord in check_dict[puz_no]:
                    if coord != poss_coord and coord in box or self.isAnyConflict(puz_no, poss_coord) and check_dict is not self.num_dict:
                        return False
                    else: continue
        return True
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
    def newGuessSet(self):
        num_poss_list = []
        guess_options = []
        for num in self.poss_dict:
            if len(self.poss_dict[num]) > 1:
                num_poss_list.append((len(self.poss_dict[num]), num))
            else: continue
        try_num = min(num_poss_list)[1]
        for trycrd in self.poss_dict[try_num]:
            for box in range(len(self.boxes)):
                if trycrd in self.boxes[box]:
                    box_crds = [trycrd]
                    for otherboxcrd in self.poss_dict[try_num]:
                        if otherboxcrd != trycrd and otherboxcrd in self.boxes[box] and otherboxcrd not in box_crds:
                            box_crds.append(otherboxcrd)
                    if len(box_crds) > 1:
                        guess_options.append((len(box_crds), box_crds))
            for row in range(len(self.puzzle_list)):
                if row == trycrd[0]:
                    row_crds = [trycrd]
                    for otherrowcrd in self.poss_dict[try_num]:
                        if otherrowcrd != trycrd and otherrowcrd[0] == row and otherrowcrd not in row_crds:
                            row_crds.append(otherrowcrd)
                    if len(row_crds) > 1:
                        guess_options.append((len(row_crds), row_crds))
            for col in range(len(self.puzzle_list)):
                if col == trycrd[1]:
                    col_crds = [trycrd]
                    for othercolcrd in self.poss_dict[try_num]:
                        if othercolcrd != trycrd and othercolcrd[1] == col and othercolcrd not in col_crds:
                            col_crds.append(othercolcrd)
                    if len(col_crds) > 1:
                        guess_options.append((len(col_crds), col_crds))
        guess_elmnt = (try_num, min(guess_options)[1])
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
    def guessIt(self):
        self.is_guess = True
        poss_count = sum(len(self.poss_dict[no]) for no in self.poss_dict)
        if len(self.solved_coords) < 81 and poss_count > 1 and not self.setExhausted:
            self.newGuessSet()
        elif len(self.solved_coords) < 81 and poss_count == 0 or self.setExhausted:
            if self.guessAmt[-1] < len(self.guessSets[-1][1]):
                self.setExhausted = False
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
            else:
                self.setExhausted = True
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
                self.guessAmt.pop(-1)
                self.guessSets.pop(-1)
                self.guessDependElim.pop(-1)
                self.new_elims = 1
        else:
            self.onlyOnes()
            self.new_elims = 0
    def attempt_solve(self):
        for num in self.num_dict:
            for scrd in self.num_dict[num]:
                if scrd not in self.solved_coords:
                    self.solved_coords.append(scrd)
        start_amt = len(self.solved_coords)
        for num in self.poss_dict:
            for r in range(len(self.puzzle_list)):
                for c in range(len(self.puzzle_list[r])):
                    if not self.isAnyConflict(num, (r, c)):
                            self.poss_dict[num].append((r, c))   
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