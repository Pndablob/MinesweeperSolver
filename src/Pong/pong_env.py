import turtle as t
import random as rand
import numpy as np


class Paddle:
    def __init__(self, vel):
        self.vel = vel
        self.done = False
        self.reward = 0
        self.hit, self.miss = 0, 0

        # Background
        self.win = t.Screen()
        self.win.title('Pong! - RL Example')
        self.win.bgcolor('black')
        self.win.setup(width=600, height=600)
        self.win.tracer(0)

        # Paddle
        self.paddle = t.Turtle()
        self.paddle.speed(0)
        self.paddle.shape('square')
        self.paddle.shapesize(stretch_wid=1, stretch_len=5)
        self.paddle.color('white')
        self.paddle.penup()
        self.paddle.goto(0, -275)

        # Ball
        self.ball = t.Turtle()
        self.ball.speed(0)
        self.ball.shape('circle')
        self.ball.color('red')
        self.ball.penup()
        self.ball.goto(0, 100)
        self.ball_dx = self.vel             # ball horizontal velocity
        self.ball_dy = self.vel             # ball vertical velocity

        # Score
        self.score = t.Turtle()
        self.score.speed(0)
        self.score.color('white')
        self.score.penup()
        self.score.hideturtle()
        self.score.goto(0, 250)
        self.score_reset()

        # Controls
        self.win.listen()
        self.win.onkeypress(self.paddle_right, 'Right')
        self.win.onkeypress(self.paddle_left, 'Left')

    def paddle_right(self):
        x = self.paddle.xcor()
        if x < 225:
            self.paddle.setx(x+20)

    def paddle_left(self):
        x = self.paddle.xcor()
        if x > -225:
            self.paddle.setx(x-20)

    def ball_reset(self):
        self.ball.goto(0, 100)
        """self.ball_dx = np.random.uniform(0.5, 1.5) * self.vel
        if np.random.random() <= 0.5:
            self.ball_dx *= -1
        self.ball_dy = np.random.uniform(0.5, 1.5) * self.vel * -1"""

    def score_reset(self):
        self.score.clear()
        self.score.write(f"Hit: {self.hit}   Missed: {self.miss}", align='center', font=('Courier', 24, 'normal'))

    def run_frame(self):
        self.win.update()

        # Ball moving
        self.ball.setx(self.ball.xcor() + self.ball_dx)
        self.ball.sety(self.ball.ycor() + self.ball_dy)

        # Ball bounce
        if self.ball.xcor() > 290:
            self.ball.setx(290)
            self.ball_dx *= -1

        if self.ball.xcor() < -290:
            self.ball.setx(-290)
            self.ball_dx *= -1

        if self.ball.ycor() > 290:
            self.ball.sety(290)
            self.ball_dy *= -1

        # Ball miss
        if self.ball.ycor() < -290:
            self.miss += 1
            self.ball_reset()
            self.score_reset()
            self.reward -= 3
            self.done = True

        # Ball hit
        if abs(self.ball.ycor() + 250) < 2 and abs(self.paddle.xcor() - self.ball.xcor()) < 55:
            self.ball_dy *= -1
            self.hit += 1
            self.score_reset()
            self.reward += 5

    # ------------------------ AI control ------------------------

    # 0 move left
    # 1 do nothing
    # 2 move right

    def reset(self):
        self.paddle.goto(0, -275)
        self.ball.goto(0, 100)
        return [self.paddle.xcor()*0.01, self.ball.xcor()*0.01, self.ball.ycor()*0.01, self.ball_dx, self.ball_dy]

    def step(self, action):
        self.reward = 0
        self.done = False

        if action == 0:
            self.paddle_left()
            self.reward -= .075

        if action == 2:
            self.paddle_right()
            self.reward -= .075

        self.run_frame()

        state = [self.paddle.xcor()*0.01, self.ball.xcor()*0.01, self.ball.ycor()*0.01, self.ball_dx, self.ball_dy]
        return self.reward, state, self.done


if __name__ == "__main__":
    game = Paddle(vel=.1)

    while True:
        game.run_frame()
