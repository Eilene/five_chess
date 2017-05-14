import math
import json
AA = [(int(i/5)-2,int(i%5)-2) for i in range(25)]
DEP = 1

class HardAi:
    def __init__(self):
        file = open('test.csv', 'r')
        self.state_score = json.loads(file.read())
        file.close()

    def next(self,player,board):
        houxuanBoard = [[0 for j in range(15)] for i in range(15)]
        for row in range(15):
            for col in range(15):
                if board[row][col] == player:
                    board[row][col] = 1
                if board[row][col] == 3 - player:
                    board[row][col] = 2
                for aa in AA:
                    if self._hefa(row + aa[0], col + aa[1]):
                        houxuanBoard[row][col] += 1 if board[row+aa[0]][col+aa[1]] > 0 else 0
        score = 0
        for i in range(15):
            score += self._row_score(board,i,0) - self._row_score(board,i,0,rev=True)
            score += self._col_score(board,0,i) - self._col_score(board,0,i,rev=True)

        score += self._rd_score(board,0,0) - self._rd_score(board,0,0,rev=False)
        for i in range(1,15):
            score += self._rd_score(board,i,0) - self._rd_score(board,i,0,rev=False)
            score += self._rd_score(board,0,i) - self._rd_score(board,0,i,rev=False)

        score += self._ru_score(board,14,0) - self._ru_score(board,14,0,rev=False)
        for i in range(0,14):
            score += self._ru_score(board, i, 0) - self._ru_score(board, i, 0, rev=False)
        for i in range(1,15):
            score += self._ru_score(board, 14, i) - self._rd_score(board, 14, i, rev=False)

        pos,minmax = self.search(board,houxuanBoard,score,0)
        return pos



    def _hefa(self,x,y):
        if x < 0 or x >= 15 or y < 0 or y >= 15:
            return False
        return True




    #def _value(self,board):

    def _rev(self,a):
        if a==0:
            return 0
        return 3 - a

    def _row_score(self,board,row,col,rev=False):
        ret = 0
        if rev:
            for col in range(15):
                ret = ret * 3 + self._rev(board[row][col])
        else:
            for col in range(15):
                ret = ret * 3 + board[row][col]
        return self.state_score[ret]

    def _col_score(self,board,row,col,rev=False):
        ret = 0
        if rev:
            for row in range(15):
                ret = ret * 3 + self._rev(board[row][col])
        else:
            for row in range(15):
                ret = ret * 3 + board[row][col]
        return self.state_score[ret]

    def _rd_score(self,board,row,col,rev=False):
        ret = 0
        m = min(row,col)
        row -= m
        col -= m
        cnt = 0
        if rev:
            while row < 15 and col < 15:
                ret = ret * 3 + self._rev(board[row][col])
                row += 1
                col += 1
                cnt += 1
        else:
            while row < 15 and col < 15:
                ret = ret * 3 + board[row][col]
                row += 1
                col += 1
                cnt += 1
        while cnt < 15:
            ret = ret * 3 + 2
            cnt += 1
        return self.state_score[ret]

    def _ru_score(self,board,row,col,rev=False):
        ret = 0
        m = min(col,14 - row)
        col -= m
        row += m
        cnt = 0
        if rev:
            while row >= 0 and col < 15:
                ret = ret * 3 + self._rev(board[row][col])
                row -= 1
                col += 1
                cnt += 1
        else:
            while row >= 0 and col < 15:
                ret = ret * 3 + board[row][col]
                row -= 1
                col += 1
                cnt += 1
        while cnt < 15:
            ret = ret * 3 + 2
            cnt += 1
        return self.state_score[ret]

    def _delta_score(self,board,row,col):
        score = 0
        score += self._row_score(board, row, col) - self._row_score(board, row, col, rev=True)
        score += self._col_score(board, row, col) - self._col_score(board, row, col, rev=True)
        score += self._rd_score(board, row, col) - self._rd_score(board, row, col, rev=True)
        score += self._ru_score(board, row, col) - self._ru_score(board, row, col, rev=True)
        return score

    def search(self,board,houxuanBoard,score,dep):
        if dep >= DEP:
            return None,score

        pos = (0,0)
        minmax = -100000 if dep % 2 == 0 else 100000
        for row in range(15):
            for col in range(15):
                if board[row][col] == 0 and houxuanBoard[row][col] > 0:
                    old_delta_score = self._delta_score(board,row,col)
                    board[row][col] = 1
                    new_delta_score = self._delta_score(board,row,col)
                    for aa in AA:
                        if self._hefa(row + aa[0], col + aa[1]):
                            houxuanBoard[row + aa[0]][col + aa[1]] += 1
                    sub_pos,val = self.search(board,houxuanBoard,score + new_delta_score - old_delta_score,dep+1)
                    if dep % 2 == 0:
                        if val > minmax:
                            pos = (row,col)
                            minmax = val
                    else:
                        if val < minmax:
                            pos = (row,col)
                            minmax = val

                    board[row][col] = 0
                    for aa in AA:
                        if self._hefa(row + aa[0], col + aa[1]):
                            houxuanBoard[row + aa[0]][col + aa[1]] -= 1
        return pos,minmax



ai = HardAi()

board = [[0 for j in range(15)] for i in range(15)]
board[7][7] = 1
print(ai.next(2,board))
