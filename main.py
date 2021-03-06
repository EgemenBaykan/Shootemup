import pygame
import random
from os import path
import math
import time

img_dir = path.join(path.dirname(__file__), "img")
font_name = pygame.font.match_font('arial')

WIDTH = 1200
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

score = 0

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RedStar 3000")
clock = pygame.time.Clock()

lastStar = 0
starTime = 400

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
        self.health = 100
        self.isAlive = False

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
        self.image = random.choice(enemy_images)
        self.image = pygame.transform.scale(self.image, (100, 50))
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


class Boss(pygame.sprite.Sprite):
    def __init__(self, trackingPlayer: Player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'enemy2.png')), (300, 150))
        self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange(WIDTH / 1.5, WIDTH - 300)
        self.rect.y = random.randrange(150, HEIGHT - 150)
        self.speedx = random.randrange(-10, 10)
        self.speedy = random.randrange(5, 15)
        self.trackingPlayer = trackingPlayer
        self.isAlive = False
        self.health = 100
        self.shootTime = random.randrange(300, 800)
        self.lastShoot = pygame.time.get_ticks()

    def update(self):
        self.trackPlayer(self.trackingPlayer)
        if pygame.time.get_ticks() - self.lastShoot > self.shootTime:
            self.shoot()
            self.lastShoot = pygame.time.get_ticks()
        if self.health <= 0:
            self.isAlive = False
            self.kill()            
            drawText(screen, "YOU WON!!!!", 30, WIDTH / 2, HEIGHT / 2)
            drawText(screen, "Your score: " + str(score), 20, WIDTH / 2, HEIGHT / 2 + 30)
            pygame.display.flip()
            time.sleep(3)

        
    def trackPlayer(self, player):
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        distance = math.hypot(dx + 1, dy + 1)
        dx, dy = dx / distance, dy / distance
        self.rect.centery += dy * self.speedy
    
    def shoot(self):
        laser = LaserBoss(self.rect.left - 20, self.rect.centery)
        all_sprites.add(laser)
        lasers.add(laser)

class LaserBoss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.flip(laser_img, True, False)
        self.image = pygame.transform.scale(self.image, (20, 5))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speedx = 40

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.left > WIDTH:
            self.kill()

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(star_img, (15, 2))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speedx = random.randrange(10,20)
        self.speedy = 10

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.left < 0:
            self.kill()

def drawText(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE) # True = Anti-aliasing for font
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def spawnEnemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)


def spawnBoss():
    boss.isAlive = True
    all_sprites.add(boss)
    bosses.add(boss)
    boss.spawnTime = pygame.time.get_ticks()

# Load images
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "player.png")).convert()
laser_img = pygame.image.load(path.join(img_dir, "laser.png")).convert()
star_img = pygame.image.load(path.join(img_dir, "star.png")).convert()

enemy_images = []
enemy_list = ['enemy.png', 'enemy2.png', 'enemy3.png']

for img in enemy_list:
    enemy_images.append(pygame.image.load(path.join(img_dir, img)).convert())

all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
lasers = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bosses = pygame.sprite.Group()
stars = pygame.sprite.Group()

player = Player()
player.isAlive = True
all_sprites.add(player)
players.add(player)

boss = Boss(player)

for i in range(8):
    spawnEnemy()

# Game loop
running = True
while running:
    clock.tick(FPS)
    # Process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    if pygame.time.get_ticks() - lastStar > starTime:
        for a in range(100):
            star = Star(random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
            all_sprites.add(star)
            stars.add(star)
        lastStar = pygame.time.get_ticks()

    # Update
    all_sprites.update()

    hitsEnemy = pygame.sprite.groupcollide(enemies, lasers, True, True)
    hitsBoss = pygame.sprite.groupcollide(bosses, lasers, False, True)
    hitsPlayer = pygame.sprite.groupcollide(players, lasers, False, True)

    for hits in hitsPlayer:
        player.health -= 10
    
    if player.health <= 0:
        player.isAlive = False
        
    if not player.isAlive:
        drawText(screen, "YOU ARE DEAD LOSER!", 18, WIDTH / 2, HEIGHT / 2)
        drawText(screen, "Your score: " + str(score), 13, WIDTH / 2, (HEIGHT / 2) + 10)
        
    if pygame.time.get_ticks() / 1000 < 30:
        for hit in hitsEnemy:
            score += 10
            spawnEnemy()
    elif pygame.time.get_ticks() / 1000 >= 30:
        for enemy in enemies:
            enemy.kill()
            if not bosses:
                spawnBoss()
        for hits in hitsBoss:
            boss.health -= 10

    # Draw / Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    if player.isAlive:
        drawText(screen, "Score: " + str(score), 18, WIDTH / 2, 15)
        drawText(screen, "Health: " + str(player.health), 18, WIDTH / 3, 15)
    else:
        drawText(screen, "YOU ARE DEAD LOSER!!!", 18, WIDTH / 2, HEIGHT / 2)
        drawText(screen, "Your score: " + str(score), 13, WIDTH / 2, (HEIGHT / 2) + 30)
        time.sleep(2)

    pygame.display.flip()

pygame.quit()