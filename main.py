# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "img")

WIDTH = 1200
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE FIGHT")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (100,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = 50
        self.rect.bottom = HEIGHT / 2
        self.speedx = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        if keystate[pygame.K_UP]:
            self.speedy = -10
        if keystate[pygame.K_DOWN]:
            self.speedy = 10
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH / 2:
            self.rect.right = WIDTH / 2
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        laser = Laser(self.rect.right, self.rect.centery)
        all_sprites.add(laser)
        lasers.add(laser)

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(laser_img, (20, 5))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speedx = 40

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (100, 50))
        self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange(WIDTH / 1.5, WIDTH - 100)
        self.rect.y = random.randrange(10, HEIGHT - 50)
        self.speedx = random.randrange(-5, 5)
        self.speedy = random.randrange(-7, 7)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH - 30:
            self.speedx = -1 * self.speedx
        if self.rect.left < WIDTH / 1.5:
            self.speedx = -1 * self.speedx
        if self.rect.top < 10:
            self.speedy = -1 * self.speedy
        if self.rect.bottom > HEIGHT - 10:
            self.speedy = -1 * self.speedy

class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy2_img, (100, 80))
        self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 40
        self.rect.x = random.randrange(WIDTH / 1.5, WIDTH - 100)
        self.rect.y = random.randrange(10, HEIGHT- 50)
        self.speedx = random.randrange(-5, 5)
        self.speedy = random.randrange(-5, 5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH - 30:
            self.speedx = -1 * self.speedx
        if self.rect.left < WIDTH / 1.5:
            self.speedx = -1 * self.speedx
        if self.rect.top < 10:
            self.speedy = -1 * self.speedy
        if self.rect.bottom > HEIGHT - 10:
            self.speedy = -1 * self.speedy

class Enemy3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy3_img, (100, 50))
        self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange(WIDTH / 1.5, WIDTH - 100)
        self.rect.y = random.randrange(10, HEIGHT - 50)
        self.speedx = random.randrange(-10, 10)
        self.speedy = random.randrange(-10, 10)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH - 30:
            self.speedx = -1 * self.speedx
        if self.rect.left < WIDTH / 1.5:
            self.speedx = -1 * self.speedx
        if self.rect.top < 10:
            self.speedy = -1 * self.speedy
        if self.rect.bottom > HEIGHT - 10:
            self.speedy = -1 * self.speedy

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "player.png")).convert()
laser_img = pygame.image.load(path.join(img_dir, "laser.png")).convert()
enemy_img = pygame.image.load(path.join(img_dir, "enemy.png")).convert()
enemy2_img = pygame.image.load(path.join(img_dir, "enemy2.png")).convert()
enemy3_img = pygame.image.load(path.join(img_dir, "enemy3.png")).convert()

all_sprites = pygame.sprite.Group()
lasers = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

enemy_types = [Enemy(), Enemy2(), Enemy3()]

for i in range(10):
    enemy = random.choices(enemy_types)
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    hits = pygame.sprite.groupcollide(enemies, lasers, True, True)
    for hit in hits:
        enemy = random.choices(enemy_types)
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()