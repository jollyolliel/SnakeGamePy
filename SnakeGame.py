import random

import pygame
from pygame.locals import *
import time

SIZE = 40

class Snake:
    def __init__(self, surface, length):
        self.parent_screen = surface
        self.block = pygame.image.load("resources/snake.jpg").convert()
        self.background = pygame.image.load("resources/background.jpg").convert()
        self.length = length
        self.x = [40]*length
        self.y = [40]*length
        self.direction = "right"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def draw(self):
        self.parent_screen.blit(self.background, (0, 0))
        self.parent_screen.blit(self.background, (480, 0))
        self.parent_screen.blit(self.background, (0, 480))
        self.parent_screen.blit(self.background, (480, 480))


        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "left":
            self.x[0] -= SIZE
        elif self.direction == "right":
            self.x[0] += SIZE
        elif self.direction == "up":
            self.y[0] -= SIZE
        elif self.direction == "down":
            self.y[0] += SIZE
        self.draw()

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple-removebg-preview.png")
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.x = 200
        self.y = 200

    def move(self):
        self.x = random.randint(1, 24)*SIZE
        self.y = random.randint(1, 24)*SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000,1000))
        self.winkeySans = pygame.font.Font("resources/WinkySans.ttf", 25)

        pygame.mixer.init()
        self.play_background_music()

        self.snake = Snake(self.surface, 5)
        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface, 5)
        self.apple = Apple(self.surface)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def show_game_win(self):
        self.render_background()
        line1 = self.winkeySans.render("You won! Good job.", True, (0, 0, 0))
        self.surface.blit(line1, line1.get_rect(center=(1040/2, 1040/2-20)))
        line2 = self.winkeySans.render("To play again press Enter. To exit press Escape.", True, (0, 0, 0))
        self.surface.blit(line2, line2.get_rect(center=(1040/2, 1040/2+20)))
        pygame.mixer.music.pause()

        pygame.display.flip()

    def show_game_over(self):
        self.render_background()
        line1 = self.winkeySans.render(f"Game is over! Your score is {self.snake.length}", True, (0, 0, 0))
        self.surface.blit(line1, line1.get_rect(center=(1040/2, 1040/2-20)))
        line2 = self.winkeySans.render("To play again press Enter. To exit press Escape.", True, (0, 0, 0))
        self.surface.blit(line2, line2.get_rect(center=(1040/2, 1040/2+20)))
        pygame.mixer.music.pause()

        pygame.display.flip()

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == "ding":
            sound = pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)

    def play(self):
        self.snake.walk()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        self.apple.draw()

        scorelbl = self.winkeySans.render(f"Score: {self.snake.length}", True, (0, 0, 0))
        self.surface.blit(scorelbl, (850, 10))  # Adjust position to avoid overlapping snake area

        pygame.display.flip()

        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Collision Occured"

        if not (0 <= self.snake.x[0] <= 960 and 0 <= self.snake.y[0] <= 960):
            self.play_sound("crash")
            raise "Hit the boundry error"

        if self.snake.length == 169:
            raise "Player Won"




    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT and self.snake.direction != "right":
                            self.snake.move_left()
                        if event.key == K_RIGHT and self.snake.direction != "left":
                            self.snake.move_right()
                        if event.key == K_UP and self.snake.direction != "down":
                            self.snake.move_up()
                        if event.key == K_DOWN and self.snake.direction != "up":
                            self.snake.move_down()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:

                self.show_game_over()
                pause = True
                self.reset()



            time.sleep(0.3)

if __name__ == '__main__':
    game = Game()
    game.run()