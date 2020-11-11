from setting import *
import pygame
import numpy as np


class App():

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption("SUDOKU")
        self.win.fill(WHITE)
        self.run = True
        self.selected = None
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.title = pygame.font.SysFont('Comic Sans MS', 50)
        #self.board = grid
        self.click = None
        self.unchanged = []
        self.key_input = None
        self.grid = board
        self.first_run = True

    ### run game
    def run_game(self):
        while self.run:
            self.event()
            self.game_window()

    # INPUT EVENTS (KEYPRESS, QUITGAME, MOUSEPRESS)
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                press = pygame.mouse.get_pos()
                #print("PRESSSED {}".format(press))
                if press[0] > BUTTONXPOS and press[1] > BUTTONYPOS:
                    if press[0] < (BUTTONXPOS + BUTTONWIDTH) and press[1] < (BUTTONYPOS + BUTTONHEIGHT):
                        print("DSLKDALSKJDLKJASKLDJKLASJKLDJKLASJDKLASJKLDJALKJKLJSLKJALKJDLKA")
                        self.solver()
                if press[0] < GRIDXPOS or press[1] < GRIDYPOS:
                    print("OUT OF GRID{},{}")
                    self.selected = None
                elif press[0]>(GRIDXPOS+GRIDWIDTH) or press[1]>(GRIDYPOS+GRIDHEIGHT):
                    print("OUT")
                    self.selected = None
                else:
                    x = (press[0]-GRIDXPOS)
                    y = (press[1]-GRIDYPOS)
                    click = x//CELLSIZE, y//CELLSIZE
                    if (click) not in self.unchanged:
                        self.selected = click

                        print(click)
                        #print(x,y)
                        #pygame.draw.rect(self.win,BLACK, ((press[0]-GRIDXPOS),(press[1]-GRIDYPOS), 100,100), 2)
                        # pygame.draw.rect(self.win, BLACK, (GRIDXPOS,GRIDYPOS, 450, 450), 2)
                        #self.selected(x,y)
                        #self.select(press[0], press[1])
                        self.select((click[0]*CELLSIZE)+GRIDXPOS, (click[1]*CELLSIZE)+GRIDYPOS)
                        # if press[0] > GRIDXPOS and press[0] < GRIDXPOS + 50:
                        #     self.select(press[0]//CELLSIZE, press[0]//CELLSIZE)


            if event.type == pygame.KEYDOWN:
                keypress = event.key
                if keypress >=32 and keypress<=126:
                    key = chr(keypress)
                    if key in ['0','1','2','3','4','5','6','7','8','9']:
                        print(key)
                        self.key_input = key

    ### Window which game runs in
    def game_window(self):
        self.create_grid()
        titlesurface= self.title.render("SUDOKU", False, BLACK)
        self.win.blit(titlesurface, (135,40))
        pygame.draw.rect(self.win, BLACK, (BUTTONXPOS,BUTTONYPOS, BUTTONWIDTH+1,BUTTONHEIGHT+1))
        pygame.draw.rect(self.win, LIGHTYELLOW, (BUTTONXPOS,BUTTONYPOS, BUTTONWIDTH,BUTTONHEIGHT))
        buttonname = self.font.render("SOLVE", False, BLACK)
        self.win.blit(buttonname, (45, 115))

        if self.first_run == True:
            self.get_unchanged()
        else:
            self.updateBoard()
            self.fillgrid()
        # self.updateBoard()
        pygame.display.update()


    ### ADDS INPUTED SUDOKU VALUE INTO BOARD
    def updateBoard(self):
        selected = self.selected
        if self.key_input:
            if (int(selected[1]), int(selected[0]) not in self.unchanged):
                self.event()
                print("CHECKING {},{}".format(int(selected[1]), int(selected[0])))
                print("CHECK KEY {}".format(int(self.key_input)))
                print(f"INSERTING KEYYYYYYYYYYYYYYYYYYYY {int(self.key_input)}")
                check_board = self.check(selected,int(self.key_input))
                if check_board == True or self.key_input == '0':
                    self.grid[int(selected[1])][int(selected[0])] = int(self.key_input)
                    print(self.grid)
                    self.fillgrid()
                    self.key_input = None
                else:
                    print("ERRORR")
                    self.key_input = None

    ### CHECKS IF INPUTED VALUE IS A LEGAL MOVE
    # INPUTS: selected position as tuple, number which is being vompared
    def check(self, selected, num):
        y = int(selected[1])
        x = int(selected[0])
        check_case = True
        for row in range(0,9):
            if self.grid[y][row] == num:
                check_case = False
                return check_case

        for column in range(0,9):
            if self.grid[column][x] == num:
                check_case = False
                return check_case

        r = (y//3)*3
        c = (x//3)*3
        for box_y in range(0,3):
            for box_x in range(0,3):
                if self.grid[r+box_y][c+box_x] == num:
                    check_case = False
                    return check_case
        return check_case

    ### FILLS SUDOKU BOARD
    def fillgrid(self):
        for y in range(0,9):
            for x in range(0,9):
                if self.grid[y][x] == 0:
                    continue
                else:
                    if (x,y) in self.unchanged:
                        txt = self.font.render(str(self.grid[y][x]), False, BLACK)
                        self.win.blit(txt, ((x*CELLSIZE)+GRIDXPOS + 15, (y*CELLSIZE)+GRIDYPOS+8))
                    else:
                        textsurface = self.font.render(str(self.grid[y][x]), False, GREY)
                        self.win.blit(textsurface, ((x*CELLSIZE)+GRIDXPOS + 15, (y*CELLSIZE)+GRIDYPOS+8))
                        pygame.display.update()


    ### HIGHLIGHTS THE SELECTED POSITION
    def select(self, x, y):
        self.win.fill(WHITE)
        pygame.draw.rect(self.win, RED, (x,y,CELLSIZE,CELLSIZE))
        pygame.display.update()


    ### SOLVES THE SUDOKU BOARD USING BACKTRACKING ALGORITHIM
    def solver(self):
        print(np.matrix(self.grid))
        for column in range(0,9):
            for row in range(0,9):
                if self.grid[column][row] == 0:
                    for number in range(1,10):
                        checker = self.check((row, column), number)
                        if checker:
                            self.grid[column][row] = number
                            self.solver()
                            self.grid[column][row] = 0

                    return True
        print(np.matrix(self.grid))
        self.fillgrid()

    #### FINDS VALUES IN SUDOKU BOARD THAT ARE ALLREADY FILLED IN FROM START
    def get_unchanged(self):
        for y in range(0,9):
            for x in range(0,9):
                if self.grid[y][x] == 0:
                    continue
                else:
                    self.unchanged.append((x, y))
        print(self.unchanged)
        self.first_run = False

    ### CREATES GRID LINES
    def create_grid(self):
        pygame.draw.rect(self.win, BLACK, (GRIDXPOS,GRIDYPOS, 450, 450), 2)
        for x in range(0,9):
            pygame.draw.line(self.win, GREY, ((GRIDXPOS+ x*CELLSIZE), GRIDYPOS), ((GRIDXPOS +x*CELLSIZE), GRIDHEIGHT+GRIDYPOS))
        for x in range(0,9):
            pygame.draw.line(self.win, GREY, (GRIDXPOS, (GRIDYPOS + x*CELLSIZE)), ((GRIDWIDTH+GRIDXPOS), (GRIDYPOS + x*CELLSIZE)))
        for x in range(0,9, 3):
            pygame.draw.line(self.win, BLACK, ((GRIDXPOS+ x*CELLSIZE)+CELLSIZE*3, GRIDYPOS), ((GRIDXPOS +x*CELLSIZE)+CELLSIZE*3, GRIDHEIGHT+GRIDYPOS))
        for x in range(0,9,3):
            pygame.draw.line(self.win, BLACK, (GRIDXPOS, (GRIDYPOS + x*CELLSIZE)+CELLSIZE*3), ((GRIDWIDTH+GRIDXPOS), (GRIDYPOS + x*CELLSIZE)+CELLSIZE*3))
        # for x in range(0,GRIDWIDTH,CELLSIZE):
        #     pygame.draw.line(self.win, GREY, (x,GRIDYPOS), (x,GRIDHEIGHT+GRIDYPOS))
