import math
state_score = []
LIVE_FIVE = 100000
LIVE_FOUR = 10000
LIVE_THREE = 1000
LIVE_TWO = 100
LIVE_ONE = 10
DEATH_FOUR = 1000
DEATH_THREE = 100
DEATH_TWO = 10

def score_state():
    for i in range(0,int(math.pow(3,15))):
        c = i
        j = []
        j.append(str(c%3))
        c = c/3
        while(c!=0):
            j.append(str(c%3))
            c = c/3
        j = j + ['0']*(15-len(j))
        s = ''.join(j)
        score = eval_score(s)
        state_score.append(score)
        if i % 100000 == 0:
            print s,score

def eval_score(s):
    #011110
    score = 0
    score += LIVE_FIVE * s.count('11111')
    score += LIVE_FOUR * s.count('011110')
    score += LIVE_THREE * (s.count('01110') + s.count('011010')+ s.count('010110'))
    score += LIVE_TWO * (s.count('01100') + s.count('00110') + s.count('01010'))
    score += LIVE_ONE * (s.count('01000') + s.count('00100') + s.count('00010'))

    score += DEATH_FOUR * (s.count('211110') + s.count('011112'))
    score += DEATH_THREE * (s.count('211100') + s.count('001112') + s.count('210110') + s.count('211010') + s.count('010112') + s.count('011012'))
    score += DEATH_TWO * (s.count('211000') + s.count('000112') + s.count('210100') + s.count('001012'))

    return score

score_state()
file = open('test.csv','w')
import json
file.write(json.dumps(state_score))
file.close()
