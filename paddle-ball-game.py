import random
import time
from dataclasses import dataclass
from tkinter import *

DURATION = 0.01

WALL_EAST = 400
WALL_SOUTH = 600

PADDLE_X0 = WALL_EAST/2-50
PADDLE_Y0 = WALL_SOUTH-100
BALL_X0 = WALL_EAST/2
#speed
PAD_VX = 10
PAD_VY = 10
BALL_VX = 2
BALL_VY = 2

COLORS = ["violet", "purple", "pink", "plum"]


# スコア処理
score = 0
ADD_SCORE = 1

# Game Controll
@dataclass
class Game:
    start: int # Spaceが押されたらStartするためのフラグ相当


def game_start(event):
    game.start = True


# Paddle
@dataclass
class Paddle:
    id: int
    x: int
    y: int
    w: int
    h: int
    vx: int
    vy: int
    c: str


def make_paddle(x, y, w=100, h=20, c="magenta"):
    id = canvas.create_rectangle(x, y, x + w, y + h, fill=c, outline=c)
    return Paddle(id, x, y, w, h, 0, 0, c)


def move_paddle(pad):
    pad.x += pad.vx
    pad.y += pad.vy


def redraw_paddle(pad):
    canvas.coords(pad.id, pad.x, pad.y, pad.x + pad.w, pad.y + pad.h)


def change_paddle_color(paddle, c="purple"):
    canvas.itemconfigure(paddle.id, fill=c)
    canvas.itemconfigure(paddle.id, outline=c)
    redraw_paddle(paddle)


# イベント処理のループに登録するハンドラX3
def left_paddle(event):
    paddle.vx = -PAD_VX


def right_paddle(event):
    paddle.vx = PAD_VX

def up_paddle(event):
    paddle.vy = -PAD_VY


def down_paddle(event):
    paddle.vy = PAD_VY



def stop_paddle(event):
    paddle.vx = 0
    paddle.vy = 0


# Ball
@dataclass
class Ball:
    id: int
    x: int
    y: int
    d: int
    vx: int
    vy: int
    c: str


def make_ball(x, y, d, vx, vy, c="lime"):
    id = canvas.create_oval(x, y, x + d, y + d, fill=c, outline=c)
    return Ball(id, x, y, d, vx, vy, c)


def move_ball(ball):
    ball.x += ball.vx
    ball.y += ball.vy


def redraw_ball(ball):
    canvas.coords(ball.id, ball.x, ball.y, ball.x + ball.d, ball.y + ball.d)





# Spear:
@dataclass
class Spear:
    id: int
    x: int
    y: int
    w: int
    h: int
    vy: int
    c: str


def make_spear(x, y, w=20, h=35, vy=5, c="#FF6666"):
    id = canvas.create_oval(x, y, x+w, y+h, fill=c, outline=c)
    return Spear(id, x, y, w, h, vy, c)




def delete_spear(spear):
    canvas.delete(spear.id)


def move_spear(spear):
    spear.y += spear.vy


def redraw_spear(spear):
    canvas.coords(spear.id, spear.x, spear.y, spear.x + spear.w, spear.y + spear.h)


# Game Over時のテキスト表示
def game_over():
    canvas.create_text(WALL_EAST/2, 150, text="Ganbarinasai^_^", font=('FixedSys', 25), fill="#008299")
    tk.update()
    time.sleep(3)


# Wall
def make_walls(ox, oy, width, height):
    canvas.create_rectangle(ox, oy, ox + width, oy + height)
    # オブジェクトを管理する必要がないので戻り値はなし


# Canvas
tk = Tk()
tk.title("Game")

canvas = Canvas(tk, width=WALL_EAST, height=WALL_SOUTH, bd=0, highlightthickness=0, bg="#dad9ff")
canvas.pack()
tk.update()

game = Game(False)  # Gameの要素は1つだけなので引数も1つ

make_walls(0, 0, WALL_EAST, WALL_SOUTH)

paddle = make_paddle(PADDLE_X0, PADDLE_Y0)
ball = make_ball(BALL_X0, 50, 10, BALL_VX, BALL_VY)


canvas.bind_all("<KeyPress-space>", game_start)
canvas.bind_all("<KeyPress-Left>", left_paddle)
canvas.bind_all("<KeyPress-Right>", right_paddle)
canvas.bind_all("<KeyPress-Up>", up_paddle)
canvas.bind_all("<KeyPress-Down>", down_paddle)
canvas.bind_all("<KeyRelease-Left>", stop_paddle)
canvas.bind_all("<KeyRelease-Right>", stop_paddle)
canvas.bind_all("<KeyRelease-Up>", stop_paddle)
canvas.bind_all("<KeyRelease-Down>", stop_paddle)

# スコア表示用テキスト領域の作成
font_style = ("Arial", 120, "bold","italic")
id_score = canvas.create_text(WALL_EAST/2, 250, text=(str(score)) ,font=font_style, fill="grey")
font_style = ("Arial", 60, "bold","italic")
title = canvas.create_text(WALL_EAST/2, 350, text=("like"), font=font_style, fill="grey")
# Spearの初期化
spear = None

# Spaceキーの入力待ち
id_text = canvas.create_text(WALL_EAST/2, 100, text="Press 'Space' to start", font=('FixedSys', 16))
tk.update()

while not game.start:
    tk.update()
    time.sleep(DURATION)

canvas.delete(id_text)
tk.update()

while True:
    move_paddle(paddle)
    move_ball(ball)

    # Spearの生成（左右の位置はランダム）
    if spear is None and random.random() < 0.01:
        spear = make_spear(random.randint(100, WALL_EAST-100), 10)
    # Spearの消去
    if spear and spear.y + spear.h >= WALL_SOUTH:
        delete_spear(spear)
        spear = None
    # Separの移動
    if spear: move_spear(spear)

    if ball.x + ball.vx <= 0 or ball.x + ball.vx >= WALL_EAST:
        ball.vx = -ball.vx
    if ball.y + ball.vy <= 0:
        ball.vy = -ball.vy
    if ball.y + ball.d + ball.vy >= WALL_SOUTH: #教科書に合わせて変更
        game_over()
        break  # Game is over
    # Hitting a spear
    if spear:
        if(paddle.x <= spear.x <= paddle.x + paddle.w and spear.y + spear.h >= paddle.y and spear.y <= paddle.y + paddle.h):
            redraw_paddle(paddle)
            redraw_spear(spear)
            game_over()
            break

    # Hitting the paddle ちょっと変更
    if paddle.x <= ball.x + ball.d and ball.x <= paddle.x + paddle.w:
        if ball.y + ball.d <= paddle.y <= ball.y + ball.d + ball.vy:
            change_paddle_color(paddle, random.choice(COLORS))
            ball.vy = -ball.vy
            ball.vx *= 1.4
            score += ADD_SCORE
            canvas.itemconfigure(id_score, text= str(score))



    # draw image
    redraw_paddle(paddle)
    redraw_ball(ball)
    if spear: redraw_spear(spear)

    tk.update()
    time.sleep(DURATION)
