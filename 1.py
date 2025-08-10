import pygame as pg
import random as rnd
import sys

# 初始化
pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption('贪吃蛇')
font = pg.font.Font(None, 36)

# 蛇与食物的实体参数
r_snake = 20
r_food = 5

# 颜色定义
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# 概率分布数据准备
_x_ = list(range(801))
_y_ = list(range(601))
_x1_ = [-((i - 400) ** 2 / 160000) + 1 for i in _x_]
_y1_ = [-((i - 300) ** 2 / 90000) + 1 for i in _y_]

# 归一化概率分布
x_prob = [p / sum(_x1_) for p in _x1_]
y_prob = [p / sum(_y1_) for p in _y1_]

class Snake:
    def __init__(self):
        self.head = [400, 300]
        self.body = [self.head.copy()]
        self.direction = "RIGHT"
        self.new_dir = "RIGHT"
        self.boost_speed = False
        self.base_speed = 10
        self.boost_speed_value = 20
        self.normal_head_color = green
        self.boost_head_color = yellow
    def move(self):
        if self.new_dir == "UP" and self.direction != "DOWN":
            self.direction = self.new_dir
        elif self.new_dir == "DOWN" and self.direction != "UP":
            self.direction = self.new_dir
        elif self.new_dir == "LEFT" and self.direction != "RIGHT":
            self.direction = self.new_dir
        elif self.new_dir == "RIGHT" and self.direction != "LEFT":
            self.direction = self.new_dir

        new_head = self.head.copy()
        if self.direction == "UP":
            new_head[1] -= r_snake
        elif self.direction == "DOWN":
            new_head[1] += r_snake
        elif self.direction == "LEFT":
            new_head[0] -= r_snake
        elif self.direction == "RIGHT":
            new_head[0] += r_snake

        self.body.insert(0, new_head)
        self.head = new_head

    def draw(self):
        for idx, segment in enumerate(self.body):
            if idx == 0:
                # 根据加速状态选择头部颜色
                color = self.boost_head_color if self.boost_speed else self.normal_head_color
            else:
                color = (0, 200, 0)
            pg.draw.rect(screen, color, (*segment, r_snake, r_snake))
class Food:
    def __init__(self, max_foods=99):
        self.foods = []
        self.max_foods = max_foods
        for _ in range(self.max_foods):
            self.foods.append(self.generate_position())

    def generate_position(self):
        while True:
            x = rnd.choices(_x_, weights=x_prob)[0]
            y = rnd.choices(_y_, weights=y_prob)[0]
            if all(abs(x - seg[0]) > r_snake or abs(y - seg[1]) > r_snake for seg in snake.body):
                return (x, y)

    def add_new_food(self):
        while len(self.foods) < self.max_foods:
            self.foods.append(self.generate_position())

    def draw(self):
        for food in self.foods:
            pg.draw.circle(screen, red, (food[0] + r_food, food[1] + r_food), r_food)

def show_score(score):
    text = font.render(f"分数: {score}", True, white)
    screen.blit(text, (10, 10))

def game_over():
    text = font.render("Game Over", True, red)
    screen.blit(text, (250, 300))
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                main()

def main():
    global snake
    snake = Snake()
    food = Food(max_foods=99)
    clock = pg.time.Clock()
    score = 0
    running = True

    while running:
        current_speed = snake.boost_speed_value if snake.boost_speed else snake.base_speed
        clock.tick(current_speed)

        # 统一事件处理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    snake.new_dir = "UP"
                elif event.key == pg.K_DOWN:
                    snake.new_dir = "DOWN"
                elif event.key == pg.K_LEFT:
                    snake.new_dir = "LEFT"
                elif event.key == pg.K_RIGHT:
                    snake.new_dir = "RIGHT"
                if event.key in (pg.K_LSHIFT, pg.K_RSHIFT):
                    snake.boost_speed = True
            if event.type == pg.KEYUP:
                if event.key in (pg.K_LSHIFT, pg.K_RSHIFT):
                    snake.boost_speed = False

        snake.move()

        # 食物碰撞检测
        eaten = False
        for fd in food.foods[:]:
            if abs(snake.head[0] - fd[0]) < r_snake and abs(snake.head[1] - fd[1]) < r_snake:
                score += 10
                food.foods.remove(fd)
                eaten = True
        if eaten:
            food.add_new_food()
        else:
            if len(snake.body) > 1:
                snake.body.pop()

        # 边界和自碰检测
        if (snake.head[0] < 0 or snake.head[0] >= 800 or
            snake.head[1] < 0 or snake.head[1] >= 600):
            game_over()
        for segment in snake.body[1:]:
            if snake.head == segment:
                game_over()

        # 绘制画面
        screen.fill(black)
        snake.draw()
        food.draw()
        show_score(score)
        pg.display.flip()

if __name__ == "__main__":
    main()