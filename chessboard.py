# -*- coding:UTF－8 -*-

#   先写棋盘函数,0代表没有，1黑2白,15*15的棋盘
Chess_rows = 15
Chess_columns = 15
Live_five = 100000
Live_four = 10000
Live_three = 1000
Live_two = 100
Live_one = 10
Death_four = 1000
Death_three = 100
Death_two = 10
class chessboard:
    def __init__(self):
        self.board = [[0 for i in range(Chess_rows)] for j in range(Chess_columns)]
        self.board[6][6] = 1#AI 为先手，先在中间下一枚棋子


    def display(self):#展示棋盘
        signal = ['.','O','X']
        row_count = 0
        content = '  A B C D E F G H I J K L M N O\n'
        for row in self.board:
            line = ' '.join([signal[n] for n in row])
            content += chr(ord('A')+row_count)+" "+line+'\n'
            row_count += 1
        return content

    def check_win(self,color):#判断是否产生胜者,在每个棋手下完后，只需要判断当前棋手是否胜利
        #遍历当前棋手下每个子判断是否成功，从上到下，从左到有遍历，则只需要遍历四个方向
        dirs = ((0,1),(1,-1),(1,0),(1,1))
        for i in range(Chess_columns):
            for j in range(Chess_columns):
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

class chessai:
    def __init__(self,depth,board):
        #传人棋盘，颜色和搜索深度,ai 为先手
        self.depth = depth
        self.color = 1
        self.board = board
        self.best_step = (-10,-10)
        self.step = ( (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1) )

    def potential_step(self):
        # 返回潜在的位置，然后计算每个位置的得分，找到得分最大的位置
        #为加快速度，只把有棋子相邻的位置为潜在位置
        steps = []
        for i in range(Chess_rows):
            for j in range(Chess_columns):
                if(self.board[i][j] != 0):
                    continue
                flag = False #标记是否四周有落子
                for k in self.step:
                    if((i+k[0])>=0 and (i+k[0])<15 and(j+k[1]>=0) and (j+k[1]<15) and self.board[i+k[0]][j+k[1]] != 0):
                        flag = True
                        break
                if(flag == False):#四周没有落子，不考虑
                    continue
                steps.append([i,j])#暂时不考虑是否越靠近中心子权重越高,所有位置分数初始化为0
        return steps

    def board_to_str(self):
        board_string = ''
        for row in self.board:
            for column in row:
                board_string += str(column)
        str_board = []
        length = len(board_string)
        i = 0
        while(i<Chess_columns*Chess_rows):
            str_board.append(board_string[i:i+Chess_columns])
            i = i+Chess_columns
        i = 1
        while(i<Chess_columns):
            str_board.append(board_string[i:length:Chess_columns])
            i += 1
        #左下到右上，只需要纪录元素大于的斜就可以
        i = 4
        while(i<Chess_columns):
            str_board.append(board_string[i:i*Chess_columns+1:Chess_columns-1])
            i += 1
        i = 1#过了对角线最长的，从第2行开始
        while(i<Chess_rows-4):
            str_board.append(board_string[(i+1)*Chess_columns-1:length:Chess_columns-1])
            i += 1
        #左上到右下
        i = 0
        while(i<Chess_columns-4):
            str_board.append(board_string[i:(Chess_rows-i)*Chess_columns:Chess_columns+1])
            i += 1
        i = 1
        while(i<Chess_rows-4):
            str_board.append(board_string[i*Chess_columns:length:Chess_columns+1])
            i += 1

        return str_board

    def eval(self,color,next_color):#评估当前棋盘对color子的得分，现在轮到color下子,nextcolor为对手
        # 计算color中活四活三等的个数，减去对手的个数得分，极为对于color的棋盘得分
        #把棋盘组织成n个字符串，计算每种规则的字符串在字符串中的个数即可,如'01110'在数组的个数极为活三的个数
        str_board = self.board_to_str()
        # 计算对手得分
        next_color_score = 0
        color_score = 0
        for i in str_board:
            if(str(next_color)*5 in i):
                return -Live_five;#对手胜利直接返回
            if(str(color)*5 in i):#轮到color，成五和活四和death four都是一样的
                return Live_five
            # next_color_score += Live_four*0.5 * i.count(str(next_color) * 2 + '0' + str(next_color) * 2)  # 11011
            # next_color_score += Live_four*0.5 * i.count(str(next_color) + '0' + str(next_color) * 3)  # 10111
            # next_color_score += Live_four*0.5 * i.count(str(next_color) * 3 + '0' + str(next_color))  # 11101
            # next_color_score += Live_three*0.5 * i.count('0' + str(next_color) + '0' + str(next_color) * 2 + '0')  # 010110
            # next_color_score += Live_three*0.5 * i.count('0' + str(next_color) * 2 + '0' + str(next_color) + '0')  # 011010
            
            next_color_score += Live_four * i.count('0' + str(next_color) * 4 + '0')#计算活四的个数
            next_color_score += Live_three * i.count('0' + str(next_color) * 3 + '0')  # 计算活三的个数
            next_color_score += Live_two * i.count('0' + str(next_color) * 2 + '0')  # 计算活二的个数
            next_color_score += Live_one * i.count('0' + str(next_color) * 1 + '0')  # 计算活一的个数
            next_color_score += Death_four * (i.count(str(color) + str(next_color) * 4 + '0') + i.count('0' + str(next_color) * 4 + str(color)))
            next_color_score += Death_three * (i.count(str(color) + str(next_color) * 3 + '0') + i.count('0' + str(next_color) * 3 + str(color)))
            next_color_score += Death_two * (i.count(str(color) + str(next_color) * 2 + '0') + i.count('0' + str(next_color) * 2 + str(color)))

            #现在轮到color下棋，所以color的活三相当于活四,活四和死四都相当于成五
            #没考虑11011，10111，11101，010110，011010，01010，
            color_score += 3 * Live_four*0.5 * i.count(str(color)*2 + '0' + str(color)*2)#11011
            color_score += 3 * Live_four*0.5 * i.count(str(color) + '0' + str(color) * 3)#10111
            color_score += 3 * Live_four*0.5 * i.count(str(color)*3 + '0' + str(color))#11101
            color_score += 3 * Live_three*0.5 * i.count('0' + str(color) +'0'+str(color)*2+'0')#010110
            color_score += 3 * Live_three*0.5 * i.count('0' + str(color)*2+'0'+str(color)+'0')#011010

            color_score += 3 * Live_four * i.count('0' + str(color) * 4 + '0')  # 计算活四的个数
            color_score += 3 * Live_three * i.count('0' + str(color) * 3 + '0')  # 计算活三的个数
            color_score += 3 * Live_two * i.count('0' + str(color) * 2 + '0')  # 计算活二的个数
            color_score += 3 * Live_one * i.count('0' + str(color) * 1 + '0')  # 计算活一的个数
            color_score += 13 * Death_four * (i.count(str(next_color) + str(color) * 4 + '0') + i.count('0' + str(color) * 4 + str(next_color)))
            color_score += 3 * Death_three * (i.count(str(next_color) + str(color) * 3 + '0') + i.count('0' + str(color) * 3 + str(next_color)))
            color_score += 3 * Death_two * (i.count(str(next_color) + str(color) * 2 + '0') + i.count('0' + str(color) * 2 + str(next_color)))

        return color_score - next_color_score


    def deep_search(self,color,next_color,depth):
        #当搜索深度为0时，返回当前棋盘对color的评估值
        if(depth<=0):
            score = self.eval(color,next_color)
            return score
        score = self.eval(color,next_color)
        if(abs(score) >= Live_five):#已经产生胜者
            return score

        # 先找到潜在位置
        best_score = -10000
        steps = self.potential_step()
        if(len(steps)<=0):
            self.best_step = [7,7]
            return
        best_step = steps[0]
        # 计算每个潜在位置的得分
        for row,column in steps:
            self.board[row][column] = color#假设走了这一步
            score = -self.deep_search(next_color,color,depth-1)#还没考虑alpha,beta剪枝
            self.board[row][column] = 0#退回这一步
            if(score > best_score):
                best_score = score
                best_step = (row,column)

        if(depth == self.depth):
            self.best_step = best_step

        return best_score


    def get_best_step(self):
        # 根据棋盘和搜索深度返回最优的移动位置,为了递归深度
        best_score = self.deep_search(1,2,self.depth)
        print best_score
        return self.best_step


def start_game(depth):
    chess = chessboard()
    ai = chessai(depth, chess.board)

    while(True):
        print chess.display()
        while(True):#收到一次合法输入则结束这层循环
            print "please input your step(字母坐标):(-1 for exit):",
            move = raw_input().strip('\r\n\t ')
            if(move == "-1"):
                return 0
            else:
                if(len(move) == 2):#输入的是合法的位置
                    row = ord(move[0].upper())-ord('A')
                    column = ord(move[1].upper())-ord('A')
                    if(row>=0 and row<15 and column>=0 and column<15):
                        if(chess.board[row][column] == 0):
                            chess.board[row][column] = 2
                            break
                        else:
                            print "cann't move here,has already a chess"
                            continue
                    else:
                        print "unlegal input,input again"
                        continue
                else:
                    print "unlegal input,input again"
                    continue

        #到这儿已经接收了合法输入，首先判断是否产生获胜方
        if(chess.check_win(2)):
            print chess.display()
            print "YOU WIN!!"
            return 0

        # 然后开始由AI下棋，评价函数
        #遍历每一个位置，计算每个位置的评价函数得分
        print "it's AI's turn ,I am thinking ",
        score,step = ai.get_best_step()
        print (score,step)
        chess.board[step[0]][step[1]] = 1

        #判断AI是否胜利
        if(chess.check_win(1)):
            print chess.display()
            print "SORRY,YOU LOOSE!!"
            return 0


if __name__ == "__main__":
    print "input难度设置：normal(1),hard(2):",
    depth = int(raw_input().strip('\r\n\t '))
    print "***********game start***************"
    start_game(depth)


