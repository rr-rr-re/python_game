import tkinter as tk
import time
from datetime import datetime
import math
import sys


class Timer:
    start_time = 0
    lap_time = 0
    end_time = 0
    result_time = 0

    count = []
    lap_time_list = []
    text1 = ""

    def start(self):
        self.start_time = time.time()
        self.lap_time = self.start_time

    def stop(self):
        self.end_time = time.time()
        self.result_time = round(self.end_time - self.start_time, 2)

    def get_string(self):
        return self.make_string(self.result_time)

    def get_string_lap(self):
        lap = time.time()
        st = self.lap_time
        self.lap_time = lap
        self.lap_time_list.append(self.make_string(round(lap - st, 2)))
        #return self.make_string(round(lap - st, 2))

    def get_count(self, index):
        self.count.append(index)

    def get(self):
        return self.result_time

    def make_string(self, result_time):
        ms, hms = math.modf(result_time)
        hour = math.floor(hms / 3600)
        mint = math.floor((hms % 3600) / 60)
        secd = math.floor(hms % 60)
        msec = math.floor(ms * 100)
        return str(hour).zfill(2) + "時間" + str(mint).zfill(2) + "分" + str(secd).zfill(2)\
        + "秒" + str(msec).zfill(2) + "ミリ秒"

    def show(self):
        print("start_time:" + self.make_string(self.start_time), \
              "\nlap_time_list:" + str(self.lap_time_list),\
              "\nend_time:" + self.make_string(self.end_time),\
              "\ntotal_time:" + self.make_string(self.result_time))

    def canvas(self):
        self.text1 = "start_time:" + self.make_string(self.start_time), \
                     "\nlap_time_list:" + str(self.lap_time_list), \
                     "\nend_time:" + self.make_string(self.end_time), \
                     "\ntotal_time:" + self.make_string(self.result_time)

win_width = 600
win_height = 480
win_center_x = win_width/2
win_text_result_y = win_height/3
win_center_y = win_height/2
win_text_posi = win_width/4
tick = 40

root = tk.Tk()
root.title(u"ブロック崩しゲーム")
root.geometry("600x480")
cv = tk.Canvas(root, width=win_width, height=win_height)
cv.pack()

# define ball
class Ball:
    x = 250
    y = 250
    w = 10

    dx = dy = 5
    color = "red"

    def draw(self):
        cv.create_oval(self.x-self.w, self.y-self.w, self.x+self.w, self.y+self.w,\
        fill = self.color, tag = "ball")
        cv.pack()

    def move(self):
        self.x += self.dx
        self.y += self.dy
#ball-wall
        if self.x - self.w < 0 or self.x + self.w > win_width:
            self.dx *= -1
        if self.y - self.w < 0 or self.y + self.w > win_height:
            self.dy *= -1
        if self.y + self.w > paddle.y - paddle.wy and ball.x >\
            paddle.x-paddle.wx and ball.x < paddle.x+paddle.wx:
            self.dy *= -1

    def delete(self):
        cv.delete("ball")

class Paddle:
    x = win_center_x
    y = win_height - 30
    wx = 45
    wy = 8
    dx = 15
    color = "blue"
    def draw(self):
        cv.create_rectangle(self.x-self.wx,self.y-self.wy,self.x+self.wx,\
        self.y+self.wy, fill = self.color, tag = "paddle")

    def right(self,event):
        cv.delete("paddle")
        self.x += self.dx
        self.draw()

    def left(self,event):
        cv.delete("paddle")
        self.x -= self.dx
        self.draw()

    def move(self):
        root.bind("<Right>",self.right)
        root.bind("<Left>",self.left)

class Block(Timer):
    w_x = 100
    w_y = 30
    global dy, score

    block_list =[[1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1]]

    def draw(self):
        for i in range(6):
            for j in range(3):
                cv.create_rectangle(i*self.w_x, j*self.w_y, (i+1)*self.w_x,\
                (j+1)*self.w_y, fill = "orange", tag = "block"+str(j)+str(i))

    def reflect(self):
        for i in range(12):
            for j in range(3):
                if (ball.y-ball.w < (j+1)*self.w_y
                    and i*self.w_x < ball.x < (i+1)*self.w_x
                    and self.block_list[j][i] == 1):
                        ball.dy *= -1
                        cv.delete("block"+str(j)+str(i))
                        timer.get_string_lap()
                        print(timer.lap_time_list)
                        self.block_list[j][i] = 0
                        score.score += 1
                        timer.get_count(score.score)
                        score.delete()
                        score.draw()

class Score():
    score = 0 #スコアの初期値
    def draw(self):
        cv.create_text(win_width - 50, 50, text = "Score = " +str(self.score),\
        font = ('FixedSys', 16), tag = "score")
    def delete(self):
        cv.delete("score")

def gameover():
    global w, dx, dy
    if ball.y + ball.w > win_height :
        cv.delete("paddle")
        cv.delete("ball")
        timer.stop()
        timer.canvas()
        timer.show()
        cv.create_text(win_center_x, win_text_result_y, text = "GAME OVER(T_T)", \
        font = ('FixedSys', 40))
        cv.create_text(win_center_x, win_center_y, text = timer.text1,\
        font = ('FixedSys', 15), width = 500)
        ball.w = 0
        ball.dx = 0
        ball.dy = 0

def gameclear():
    global w, dx, dy
    if score.score == 18 :
        cv.delete("paddle")
        cv.delete("ball")
        timer.stop()
        timer.canvas()
        timer.show()
        cv.create_text(win_center_x, win_text_result_y, text="GAME CLEAR(^0^)", \
        font=('FixedSys', 40))
        cv.create_text(win_center_x, win_center_y, text=timer.text1, \
        font=('FixedSys', 15), width = 500)
        ball.w = 0
        ball.dx = 0
        ball.dy = 0

timer = Timer()
paddle = Paddle()
ball = Ball()
block = Block()
score = Score()

ball.draw()
paddle.draw()
block.draw()
score.draw()

def gameloop():
    ball.delete()
    ball.move()
    paddle.move()
    block.reflect()
    ball.draw()
    gameover()
    gameclear()
    root.after(tick, gameloop)

timer.start()
print(timer.start_time)
gameloop()
root.mainloop()
