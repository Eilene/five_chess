# -*- coding:UTF-8 -*-
import pygame
from pygame.locals import *
from chessboard import *
from chessboard import  chessai
from hard import HardAi
import copy

LINES_NUM = 15


class Chess:
    def __init__(self,screen):
        self.screen = screen
        self.step = []
        self.color = 1
        self.winner = None
        self.w_width, self.w_height = self.screen.get_size()
        self.c_size = int(self.w_height / (LINES_NUM + 1))
        self.pos_x = int((self.w_width - self.c_size * LINES_NUM) / 2)
        self.pos_y = int((self.w_height - self.c_size * LINES_NUM) / 2)
        self.board = [[0 for i in range(LINES_NUM)] for j in range(LINES_NUM)]
        self.font = pygame.font.Font(r"../chess/client/data/font/title.TTF", 24)

    def check_win(self,color):#判断是否产生胜者,在每个棋手下完后，只需要判断当前棋手是否胜利
        #遍历当前棋手下每个子判断是否成功，从上到下，从左到有遍历，则只需要遍历四个方向
        dirs = ((0,1),(1,-1),(1,0),(1,1))
        for i in range(LINES_NUM):
            for j in range(LINES_NUM):
                if(self.board[i][j] != color):
                    continue
                for dir in dirs:
                    flag = True
                    temprow = i
                    tempcolumn = j
                    for count in range(4):
                        temprow += dir[0]
                        tempcolumn += dir[1]
                        if(not (temprow>=0 and temprow< 15 and tempcolumn>=0 and tempcolumn<15)):#越界了
                            flag = False
                            break
                        if(self.board[temprow][tempcolumn] != color):
                            flag = False
                            break
                    if(flag == True):
                        return True

        return False

    #画棋盘
    def draw(self):
        self.screen.fill((247, 227, 200))
        pygame.draw.rect(self.screen, (0, 0, 0), Rect((self.pos_x, self.pos_y), (self.c_size * LINES_NUM, self.c_size * LINES_NUM)), 2)

        for i in range(0, LINES_NUM):
            pygame.draw.line(self.screen, (128, 128, 128), (self.pos_x + i * self.c_size, self.pos_y),
                             (self.pos_x + i * self.c_size, self.pos_y + self.c_size * LINES_NUM), 1)
            pygame.draw.line(self.screen, (128, 128, 128), (self.pos_x, self.pos_y + i * self.c_size),
                             (self.pos_x + self.c_size * LINES_NUM, self.pos_y + i * self.c_size), 1)
        pygame.display.update()

    #捕捉位置并且检查是否胜利，没有胜利画上棋子
    def raw_input(self,e):
        if(self.winner==None):
            (x, y) = e.pos
            x_pos = x - (self.pos_x - int(self.c_size / 2))
            y_pos = y - (self.pos_y - int(self.c_size / 2))

            if (x_pos >= 0) and (y_pos >= 0):
                new_pos = (int(x_pos / self.c_size), int(y_pos / self.c_size))
                # print x_pos, y_pos, new_pos
                if (new_pos[0] <= LINES_NUM) and (new_pos[1] <= LINES_NUM
                        and self.board[new_pos[0]][new_pos[1]]==0):
                    # 标记发送
                    self.step = new_pos


    def draw_index(self):
        new_pos = self.step
        if(self.board[new_pos[0]][new_pos[1]] == 0):#之前没有下子
            self.board[new_pos[0]][new_pos[1]] = self.color
            if (self.check_win(self.color)):
                self.winner = self.color
            #画上棋子
            if (self.color == 1):
                pos = (
                self.pos_x + int(self.step[0]) * self.c_size, self.pos_y + int(self.step[1]) * self.c_size)
                pygame.draw.circle(self.screen, (0, 0, 0), pos, int(self.c_size / 2 - 2))
            else:
                pos = (
                self.pos_x + int(self.step[0]) * self.c_size, self.pos_y + int(self.step[1]) * self.c_size)
                pygame.draw.circle(self.screen, (255, 255, 255), pos, int(self.c_size / 2 - 2))
            if self.color == 2:
                self.color = 1
            else:
                self.color = 2



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Eilene')
        self.screen = pygame.display.set_mode((640, 480))
        self.stat = 'chess'
        self.chess = Chess(self.screen)

    def loop(self):
        ai = chessai(1,self.chess.board)
        ai2 = HardAi()
        test = chessboard()
        test.board = self.chess.board
        clock = pygame.time.Clock()
        self.chess.draw()
        color = 2
        while self.stat != 'quit':
            if(self.chess.color!= color):
                self.chess.step = ai.get_best_step()
                self.draw()  # 画下棋的位置
            color = self.chess.color

            temp = copy.deepcopy(self.chess.board)
            self.chess.step = ai2.next(2,temp)
            self.draw()  # 画下棋的位置

            # print "&****"+str(color)
            # while True:
            #     pos = self.run()
            #     if(pos!= None):
            #         break
            # self.draw()#画下棋的位置
            clock.tick(60)
            test.display()
        pygame.quit()

    def draw(self):
        self.chess.draw_index()
        if(self.chess.winner!=None):
            self.screen.blit(
                self.chess.font.render("{0} Win".format("Black" if self.chess.winner == 1 else "White"), True, (0, 0, 0)), (500, 10))
        pygame.display.update()

    def run(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT or self.chess.winner!=None:
                self.stat = 'quit'
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.chess.raw_input(e)
                return e.pos



if __name__ == '__main__':
    game = Game()
    game.loop()