from pygame import *
from random import randint
from time import sleep

init()

WIDTH = 336
HEIGHT = 540
TICKRATE = 60
WHITE = (255, 255, 255)
#RED = (255, 0, 0)
#game_over = Surface((HEIGHT, WIDTH))

window = display.set_mode((WIDTH, HEIGHT))

music = mixer.music.load('assets/Run-Amok(chosic.com).mp3')


clock = time.Clock()

class Background():
    def __init__(self):
        self.image = image.load('assets/background.png')
        self.x_1 = 0
        self.x_2 = WIDTH
        self.y = 0
    
    def draw(self):
        window.blit(self.image, (self.x_1, self.y))
        window.blit(self.image, (self.x_2, self.y))

    def update(self):
        self.x_1 -= 1
        self.x_2 -= 1
        if self.x_1 <= -WIDTH:
            self.x_1 = WIDTH
        if self.x_2 <= -WIDTH:
            self.x_2 = WIDTH


class Ground():
    def __init__(self):
        self.image = image.load('assets/ground.png')
        self.x_1 = 0
        self.x_2 = WIDTH
        self.y = HEIGHT - 100
    
    def draw(self):
        window.blit(self.image, (self.x_1, self.y))
        window.blit(self.image, (self.x_2, self.y))

    def update(self):
        self.x_1 -= 2
        self.x_2 -= 2
        if self.x_1 <= -WIDTH:
            self.x_1 = WIDTH
        if self.x_2 <= -WIDTH:
            self.x_2 = WIDTH

class Pipes():
    def __init__(self):
        self.gate = randint(100, HEIGHT - 200)
        self.gap = randint(45, 60)
        self.top_image = image.load('assets/top-pipe.png')
        self.top_rect = self.top_image.get_rect()
        self.top_rect.bottomleft = (WIDTH, self.gate - self.gap)

        self.bot_image = image.load('assets/bot-pipe.png')
        self.bot_rect = self.top_image.get_rect()
        self.bot_rect.topleft = (WIDTH, self.gate + self.gap)
    
    def draw(self):
        window.blit(self.top_image, self.top_rect)
        window.blit(self.bot_image, self.bot_rect)

    def update(self):
        self.top_rect.x -= 2
        self.bot_rect.x -= 2
        if self.top_rect.right < 0:
            self.gate = randint(100, HEIGHT - 200)
            self.gap = randint(45, 60)
            self.top_rect.bottomleft = (WIDTH, self.gate - self.gap)
            self.bot_rect.topleft = (WIDTH, self.gate + self.gap)
            
            game.score += 1
            game.update_score()

class Bird(sprite.Sprite):
    def __init__(self):
        super().__init__
        self.image_orig = image.load('assets/bird.png')
        self.image = self.image_orig
        self.rect = self.image.get_rect(center = (WIDTH // 3, HEIGHT // 2))
        self.base_speed = -2
        self.speed = self.base_speed
        self.angle = 0
        self.sound_jump = mixer.Sound('assets/pryjok-2.mp3')
        self.music_over = mixer.Sound('assets/b1314089d5efb25.mp3')
    def draw(self):
        window.blit(self.image, self.rect)
    
    def update(self, events):
        self.rect.y -= self.speed

        if self.speed > 0:
            self.angle += 3
            if self.angle > 30:
                self.angle = 30
        elif self.speed < 0:
            self.angle -= 1
            if self.angle < 45:
                self.angle = -45
        self.image = transform.rotate(self.image_orig, self.angle)

        if self.rect.y < 0:
            self.rect.y = 0
        if self.speed > self.base_speed:
            self.speed -= 1

        if self.rect.bottom > HEIGHT - 100:
            self.rect.bottom = HEIGHT - 100
        if game.state == 'play':
            for e in events:
                if e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        self.sound_jump.play()
                        self.speed = 6
            if self.rect.collidelistall([pipe.top_rect, pipe.bot_rect]):
                game.state = 'over'
                self.music_over.play()
                self.image_orig = image.load('assets/diedbird.png')
                self.angle = -45
                    
    
class GameManager():
    def __init__(self):
        self.state = 'play'
        self.score = 0
        self.font = font.Font('assets/Flappy-Bird.ttf', 50)
        self.score_text = self.font.render('0', True, WHITE)
        self.restart_text = self.font.render('Press R to restart', True, WHITE)

    def centerx(self, surf):
        return (WIDTH // 2) - (surf.get_width() // 2)

    def centery(self, surf):
        return (HEIGHT // 2) - (surf.get_height() // 2)

    def draw_score(self):
        window.blit(self.score_text, (self.centerx(self.score_text), 10))

    def update_score(self):
        self.score_text = self.font.render(str(self.score), True, WHITE)

    def draw_restart(self):
        window.blit(self.restart_text, (self.centerx(self.restart_text), self.centery(self.restart_text)))

    def restart(self):
        self.state = 'play'
        mixer.music.unpause()
        self.score = 0
        self.update_score()
        bird.image_orig = image.load('assets/bird.png')
        bird.rect.center = (WIDTH // 3, HEIGHT // 2)
        bird.speed = bird.base_speed
        bird.angle = 0
        pipe.gate = randint(100, HEIGHT - 200)
        pipe.gap = randint(45, 60)
        pipe.top_rect.bottomleft = (WIDTH, pipe.gate - pipe.gap)
        pipe.bot_rect.topleft = (WIDTH, pipe.gate + pipe.gap) 



bg = Background()
gr = Ground()
bird = Bird()
pipe = Pipes()
game = GameManager()

while True:
    events = event.get()
    for e in events:
        if e.type == QUIT:
            exit()
        if e.type == KEYDOWN:
            if e.key == K_r and game.state == 'over':
                game.restart()
            
    if game.state == 'play':
        bg.update()
        pipe.update()
        gr.update()
    bird.update(events)
    bg.draw()
    pipe.draw()
    gr.draw()
    bird.draw()
    game.draw_score()
    if game.state == 'over':
        mixer.music.play(-1)
        #game_over.fill(RED)
        mixer.music.pause()
        game.draw_restart()

    display.flip()
    clock.tick(TICKRATE)