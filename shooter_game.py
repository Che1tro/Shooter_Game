from pygame import *
import pygame.time
from random import *
import time

mixer.init()
font.init()


font_text = font.SysFont('Arial', 36)
font_final = font.SysFont('Arial', 70)
font_win = font.SysFont('Arial',70)
font_sec = font.SysFont('Arial',36)

window = display.set_mode((700, 500))
mixer.music.load('space.ogg')
fire = mixer.Sound('fire.ogg')
mixer.music.play()
display.set_caption('Космический бой')

background = transform.scale(image.load('galaxy.jpg'), (700, 500))
a = 10
p = 0
s = 0

class GameSprite(sprite.Sprite):
    def __init__(self, p_image, p_speed, p_x, p_y, s_x, s_y):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (s_x, s_y))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.y = p_y
        self.rect.x = p_x
        self.s_x = s_x
        self.s_y = s_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > -5:
            self.rect.y -= 4
        if keys_pressed[K_s] and self.rect.y < 420:
            self.rect.y += 4
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= 4 
        if keys_pressed[K_d] and self.rect.x < 600:
            self.rect.x += 4 
    def fire(self):

        bullet = Bullet("bullet.png", 4, self.rect.centerx - 7, self.rect.y, 15, 20)
        bullets.add(bullet) 
        fire.play()

class Enemy(GameSprite):
    def update(self):
        global p
        if self.rect.y <= 435:
            self.rect.y += self.speed
        else:
            p += 1
            self.rect.y = 0
            self.rect.x = randint(0, 600)
            self.speed = randint(1, 3)

class Asteroid(GameSprite):
    def update(self):
        if self.rect.y <=435:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(0, 600)
            self.speed = randint(1, 3)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

hero = Player('rocket.png', 100, 30, 435, 70, 70)
asteroids = sprite.Group()
enemies = sprite.Group()
bullets = sprite.Group()


for i in range(5):
    enemy = Enemy('ufo.png', randint(1, 2), randint(0, 600), 0, 85, 70)
    enemies.add(enemy)
for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(1, 2), randint(0, 600), 0, 85, 70)
    asteroids.add(asteroid)


clocks = pygame.time.Clock()
finish = False
rel_time = False
game = True
FPS = 60
num_fire = 0

lose_text = font_final.render('YOU LOSE!', True, (255, 0, 0))
win_text = font_win.render('YOU WIN!', True, (255, 0, 0))
sec_text = font_sec.render('WAIT RELOAD...', True, (255, 0, 0))

while game: 
    for e in event.get(): 
        if e.type == QUIT: 
            game = False 
        elif e.type == KEYDOWN and not finish and rel_time == False:
            if e.key == K_SPACE:
                hero.fire()
                num_fire +=1
            if num_fire >=5:
                rel_time = True
                start_time = time.time()
        elif rel_time == True:
            time_need = (time.time() - start_time)
            if time_need >= 3:
                rel_time = False
                num_fire = 0
    clocks.tick(FPS) 
    
    if not finish: 
        window.blit(background, (0, 0)) 
        
        hero.update()
        enemies.update()
        asteroids.update()
        bullets.update()
        if rel_time:
            window.blit(sec_text, (250, 400))
        hero.reset()
        enemies.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        

        score_surface = font_text.render('Счет: ' + str(s), 1, (255, 255, 255))
        lost_surface = font_text.render('Пропущено: ' + str(p), 1, (255, 255, 255))
        window.blit(score_surface, (10, 10))
        window.blit(lost_surface, (10, 45))
        

        collided_enemies = sprite.groupcollide(enemies, bullets, False, True)
        if sprite.spritecollideany(hero, enemies, collided=sprite.collide_rect_ratio(0.7)) or sprite.spritecollideany(
        hero, asteroids, collided=sprite.collide_rect_ratio(0.7)):
            finish = True
            p=6
        for enemy in collided_enemies:
            s += 1 
            enemy.rect.y = 0
            enemy.rect.x = randint(0, 600)
            enemy.speed = randint(1, 3)
            

        if p >= 5:
            finish = True
        elif s>= 10:
            finish = True

    else:
        
        if p >= 5:
            window.blit(lose_text, (230, 220))
        elif s >= 10:  
            window.blit(win_text, (230, 220))

    display.update()
