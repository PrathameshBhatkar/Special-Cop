"""
add crane to plats
"""
import datetime
import random
import sys

import pygame
from pygame.image import load
from pygame.mixer import Sound
from pygame.transform import scale
from pygame import Rect

pygame.mixer.init()
pygame.init()

screenHeight = 600
screenWidth = 1000
screen = pygame.display.set_mode((screenWidth, screenHeight))


class PLATFORM:
    def __init__(self):
        self.new_plat = None
        self.posix = 0
        self.plat_speed = 5
        self.plat_img = pygame.image.load('resources/wall.png').convert_alpha()

    def create_platform(self):
        self.new_plat = pygame.Rect(screenWidth + 500 + 60,
                                    random.choice([screenHeight / 2,
                                                   screenHeight / 3,
                                                   screenHeight / 4,
                                                   screenHeight / 5
                                                   ]),
                                    500, 150)

        return self.new_plat

    def move_plat(self, pipes):
        for pipi in pipes:
            pipi.centerx -= self.plat_speed
        return pipes

    def draw_plat(self, pipes):
        for pipi in pipes:
            screen.blit(self.plat_img, pipi)

    def move_bg(self):
        screen.blit(bg, (self.posix, 0))
        screen.blit(bg, (self.posix + screenWidth - 7, 0))

        if self.posix <= -screenWidth:
            self.posix = 0


class OFFICER:
    def __init__(self):

        # variables
        self.was_up = False
        self.no_Of_Bullets_In_1_Pack = 5
        self.bag_collected = 0
        self.enemy_killed_num = 0
        self.jumHeight = 8
        self.heartNum = 3
        self.bulletNum = 5
        self.cop_Movementx = 0
        self.cop_movement = 0
        self.cop_speed = 5
        self.player_score = 25
        self.gravityN = 0.30
        self.bullet_isFired = False
        self.bullet_Speed = 40
        self.enemyKillProfit = 50

        # musics
        self.ground_hit_sound = Sound('resources/audio/ground hit.wav')
        self.end_Music = Sound('resources/audio/mario die.mp3')
        self.hit_music = Sound('resources/audio/hit plat.wav')
        self.level_up_Music = Sound('resources/audio/level up.wav')
        self.jump_sound = pygame.mixer.Sound('resources/audio/jump.wav')
        self.hurt_sound = Sound('resources/audio/hurt.mp3')

        # images
        self.cop_img = pygame.image.load('resources/cop.png').convert_alpha()
        self.bullet_img_full = load('resources/bullet.png').convert_alpha()
        self.bullet_no = load('resources/no bullet.png').convert_alpha()

        self.money_bag = load('resources/money bag.png').convert_alpha()
        self.money_bag = scale(self.money_bag, (29, 45))

        self.enemy_catched = load('resources/enemy_catched.png').convert_alpha()
        self.enemy_catched = scale(self.enemy_catched, (35, 35))

        # rects
        self.cop_rect = pygame.Rect(150, screenHeight / 2, 57, 47)
        self.bullet = pygame.Rect(-1, -100, 50, 2)

        self.heart1 = Rect(35, 10, 32.69, 28.86)
        self.heart2 = Rect(35 + 35, 10, 32.69, 28.86)
        self.heart3 = Rect(35 + 35 + 35, 10, 32.69, 28.86)

        self.bullet1 = Rect(40, 50, 11, 33)
        self.bullet2 = Rect(40 + 18, 50, 11, 33)
        self.bullet3 = Rect(40 + 18 + 18, 50, 11, 33)
        self.bullet4 = Rect(40 + 18 + 18 + 18, 50, 11, 33)
        self.bullet5 = Rect(40 + 18 + 18 + 18 + 18, 50, 11, 33)

    def draw_cop(self):
        screen.blit(self.rotate_cop(self.cop_img), self.cop_rect)

    def gravity(self):
        self.cop_rect.x += self.cop_Movementx
        self.cop_movement += self.gravityN
        self.cop_rect.centery += self.cop_movement

    def timer(self, recordesd_time, curresnt_time, time=1000):
        if curresnt_time - recordesd_time >= time:
            self.cop_img = load('resources/cop.png')

    def jump(self):
        self.jump_sound.play()
        self.cop_img = load('resources/cop fly.png')
        if not (self.cop_movement <= -4) and self.cop_movement <= 15:
            self.cop_movement = 0
            self.cop_movement -= self.jumHeight
            self.was_up = True

    @staticmethod
    def draw_word(posi_xy, text, color, textSize=35, font='didot.ttc'):

        t = pygame.font.SysFont(font, textSize).render(text, False, color)
        screen.blit(t, posi_xy)

    def check_collision(self, pipes):

        if self.cop_rect.y <= 0:
            self.cop_rect.y = 0
            if self.cop_movement < -7.5:
                self.heartNum -= 0.5

        elif self.cop_rect.y >= screenHeight:
            self.cop_rect.y = screenHeight

        elif self.cop_rect.x <= 0:
            self.cop_rect.x = 0

        if self.cop_rect.x + self.cop_rect.w >= screenWidth:
            self.cop_rect.x = screenWidth - self.cop_rect.w

        for pipi in pipes:
            if self.cop_rect.colliderect(pipi):
                if abs(self.cop_rect.bottom - pipi.top) < 15:
                    self.player_score += 1
                    self.cop_rect.bottom = pipi.top
                    self.cop_movement = 0
                    if self.was_up:
                        self.ground_hit_sound.play()
                        self.was_up = False

                elif abs(self.cop_rect.top - pipi.bottom) < 15:
                    self.player_score += 1
                    self.cop_rect.top = pipi.bottom
                    self.cop_movement = 0

                elif abs(self.cop_rect.right - pipi.left) < 10:
                    self.heartNum -= 1
                    self.hurt_sound.play()
                    self.reset_cop_posi()

                    if self.heartNum <= 0:
                        self.end_Music.play()
                        restartPage()

            if self.bullet.colliderect(pipi) or self.bullet.midright == pipi.midleft:
                self.bullet.y = -100
                self.hit_music.play()

        if self.cop_rect.colliderect(floor):
            if (self.cop_rect.bottom - floor.top) < 25:
                self.cop_rect.bottom = floor.top
                self.cop_movement = 0
                if self.was_up:
                    self.ground_hit_sound.play()
                    self.was_up = False

    def fire_bullet(self):
        if self.bullet_isFired:
            self.bullet.x += self.bullet_Speed

    def draw_bullet(self):
        pygame.draw.ellipse(screen, (255, 255, 255), self.bullet)

    def enemy_and_other_stuff_counter(self):
        screen.blit(self.money_bag, (screenWidth - 150, 10))
        self.draw_word((screenWidth - 105, 15), str(self.bag_collected), (0, 0, 0), textSize=45)

        screen.blit(self.enemy_catched, (screenWidth - 150, 65))
        self.draw_word((screenWidth - 105, 70), str(self.enemy_killed_num), (0, 0, 0), textSize=45)

    def endgame(self):
        with open("data/Scores.txt", "a") as f:
            f.write(f"On {str(datetime.datetime.today())[:19]} you Killed"
                    f" {self.enemy_killed_num} enemies and collected {self.bag_collected} bags\n")

    def bullet_checkCollisions(self, enemies):
        for enemy in enemies:
            if self.bullet.colliderect(enemy):
                self.level_up_Music.play()
                self.bullet.y = -100
                self.enemy_killed_num += 1
                coin_list.append(Coin.create_coin(enemy))
                enemy_list.remove(enemy)

    def draw_hearts(self):

        if self.heartNum == 3:
            screen.blit(heart_full, self.heart1)
            screen.blit(heart_full, self.heart2)
            screen.blit(heart_full, self.heart3)

        elif self.heartNum == 2.5:
            screen.blit(heart_full, self.heart1)
            screen.blit(heart_full, self.heart2)
            screen.blit(heart_half, self.heart3)

        elif self.heartNum == 2:
            screen.blit(heart_full, self.heart1)
            screen.blit(heart_full, self.heart2)
            screen.blit(heart_no, self.heart3)

        elif self.heartNum == 1.5:
            screen.blit(heart_full, self.heart1)
            screen.blit(heart_half, self.heart2)
            screen.blit(heart_no, self.heart3)

        elif self.heartNum == 1:
            screen.blit(heart_full, self.heart1)
            screen.blit(heart_no, self.heart2)
            screen.blit(heart_no, self.heart3)

        elif self.heartNum == 0.5:
            screen.blit(heart_half, self.heart1)
            screen.blit(heart_no, self.heart2)
            screen.blit(heart_no, self.heart3)

        elif self.heartNum <= 0:
            screen.blit(heart_no, self.heart1)
            screen.blit(heart_no, self.heart2)
            screen.blit(heart_no, self.heart3)

            self.end_Music.play()
            restartPage()

    def draw_ammo(self):
        n = self.bulletNum

        if 4 < n <= 5:
            screen.blit(self.bullet_img_full, self.bullet1)
            screen.blit(self.bullet_img_full, self.bullet2)
            screen.blit(self.bullet_img_full, self.bullet3)
            screen.blit(self.bullet_img_full, self.bullet4)
            screen.blit(self.bullet_img_full, self.bullet5)

        elif 3 < n <= 4:
            screen.blit(self.bullet_img_full, self.bullet1)
            screen.blit(self.bullet_img_full, self.bullet2)
            screen.blit(self.bullet_img_full, self.bullet3)
            screen.blit(self.bullet_img_full, self.bullet4)
            screen.blit(self.bullet_no, self.bullet5)

        elif 2 < n <= 3:
            screen.blit(self.bullet_img_full, self.bullet1)
            screen.blit(self.bullet_img_full, self.bullet2)
            screen.blit(self.bullet_img_full, self.bullet3)
            screen.blit(self.bullet_no, self.bullet4)
            screen.blit(self.bullet_no, self.bullet5)

        elif 1 < n <= 2:
            screen.blit(self.bullet_img_full, self.bullet1)
            screen.blit(self.bullet_img_full, self.bullet2)
            screen.blit(self.bullet_no, self.bullet3)
            screen.blit(self.bullet_no, self.bullet4)
            screen.blit(self.bullet_no, self.bullet5)

        elif 0 < n <= 1:
            screen.blit(self.bullet_img_full, self.bullet1)
            screen.blit(self.bullet_no, self.bullet2)
            screen.blit(self.bullet_no, self.bullet3)
            screen.blit(self.bullet_no, self.bullet4)
            screen.blit(self.bullet_no, self.bullet5)

        elif -1 < n <= 0:
            screen.blit(self.bullet_no, self.bullet1)
            screen.blit(self.bullet_no, self.bullet2)
            screen.blit(self.bullet_no, self.bullet3)
            screen.blit(self.bullet_no, self.bullet4)
            screen.blit(self.bullet_no, self.bullet5)

    def rotate_cop(self, img):
        # if not (self.cop_movement < 0):
        if 1 > self.cop_movement > 0:
            new_img = pygame.transform.rotozoom(img, 0, 1)
        else:
            new_img = pygame.transform.rotozoom(img, self.cop_movement * 7, 1)

        return new_img

    def reset_cop_posi(self):
        self.cop_rect.x = 150
        self.cop_rect.y = floor.y - self.cop_rect.h - 50
        self.cop_movement = 0


class ENEMY:
    def __init__(self):
        self.enemy_spawn_num = 1
        self.enemy_wave_spawn_num = 5
        self.gravityN = 7
        self.enemy_movement = 0
        self.enemy_img = load('resources/enemy.png')
        self.new_enemy = None

    def create_enemy(self, m):
        if m:
            self.new_enemy = pygame.Rect(screenWidth + 50 + random.choice([50,
                                                                           100,
                                                                           150,
                                                                           200,
                                                                           250,
                                                                           300,
                                                                           350,
                                                                           400,
                                                                           450,
                                                                           500,
                                                                           550,
                                                                           600,
                                                                           650
                                                                           ]), random.choice([50,
                                                                                              100,
                                                                                              150,
                                                                                              260
                                                                                              ]),
                                         50, 50)
        else:
            self.new_enemy = pygame.Rect(screenWidth + 50, random.choice([50,
                                                                          100,
                                                                          150,
                                                                          260
                                                                          ]),
                                         50, 50)
        self.enemy_img = pygame.transform.scale(self.enemy_img, (self.new_enemy.w, self.new_enemy.h))

        return self.new_enemy

    @staticmethod
    def move_enemy(enemies):
        for enemy in enemies:
            enemy.centerx -= 6
            if enemy.x < -enemy.w + 20:
                enemies.remove(enemy)
        return enemies

    def draw_enemy(self, enemies):
        for enemy in enemies:
            self.enemy_check_collision(plat_list, enemy)
            screen.blit(self.enemy_img, enemy)

    def gravity(self, enemies):
        for enemy in enemies:
            if enemy.x <= screenWidth + 20:
                enemy.y += self.gravityN

    def enemy_check_collision(self, pipes, enemy):
        global enemy_list

        for pipi in pipes:
            if enemy.colliderect(pipi):
                if abs(enemy.bottom - pipi.top) < 10:
                    enemy.bottom = pipi.top
                    self.enemy_movement = 0

                elif abs(enemy.top - pipi.bottom) < 10:
                    enemy.top = pipi.bottom
                    self.enemy_movement = 0

        if enemy.colliderect(floor):
            if (enemy.bottom - floor.top) < 15:
                enemy.bottom = floor.top
                self.enemy_movement = 0

        enemy_list_copy = []
        [enemy_list_copy.append(enemy) for enemy in enemy_list if enemy not in enemy_list_copy]
        enemy_list = enemy_list_copy

        if enemy.colliderect(Officer.cop_rect):
            Officer.reset_cop_posi()
            Officer.heartNum -= 0.5
            enemy_list.remove(enemy)

            Officer.hurt_sound.play()


class COINS:
    def __init__(self):
        self.pick_coin_music = Sound('resources/audio/coin pickup.wav')
        self.gravityN = 3
        self.coin_movement = 0
        self.coin_img = load('resources/money bag.png')
        self.new_coin = None
        self.bounce_Anim = 100

    def create_coin(self, enemy):
        self.new_coin = enemy
        self.new_coin.y -= self.bounce_Anim
        self.new_coin.h = 45
        self.new_coin.w = 29
        self.coin_img = scale(self.coin_img, (self.new_coin.w, self.new_coin.h))

        return self.new_coin

    @staticmethod
    def move_coin(coins):
        for coin in coins:
            coin.centerx -= 2.5
            if coin.x < -coin.w + 20:
                coins.remove(coin)
        return coins

    def draw_coin(self, enemies):
        for coin in enemies:
            self.gravity(coin)
            self.coin_check_collision(plat_list, coin)
            self.coin_Movement(coin)
            screen.blit(self.coin_img, coin)

    def gravity(self, coin):
        # self.coin_movement += self.gravityN
        coin.centery += self.gravityN + 0.5

    def coin_check_collision(self, pipes, ammo):

        for pipi in pipes:
            if ammo.colliderect(pipi):
                if abs(ammo.bottom - pipi.top) < 10:
                    ammo.bottom = pipi.top

                    self.coin_movement = 0

                elif abs(ammo.top - pipi.bottom) < 10:
                    ammo.top = pipi.bottom
                    self.coin_movement = 0

        if ammo.colliderect(floor):
            if (ammo.bottom - floor.top) < 15:
                ammo.bottom = floor.top
                self.coin_movement = 0

        if ammo.colliderect(Officer.cop_rect):
            Officer.player_score += Officer.enemyKillProfit
            Officer.bag_collected += 1
            self.pick_coin_music.play()
            coin_list.remove(ammo)

    @staticmethod
    def coin_Movement(coin):
        pass
        coin.x -= 0


class MAIN:
    def __init__(self):
        self.music_img = load('resources/volume.png')
        self.music_img_no = load('resources/volume no.png')

        self.music_img = scale(self.music_img, (29, 25))
        self.music_img_no = scale(self.music_img_no, (29, 25))

        self.is_muted = False
        self.none = load('resources/MAIN STUFF/home page.png').convert_alpha()
        self.is_OnYes = None

        self.bga = self.none

        self.start_r = pygame.Rect(445, 349, 375, 93)
        # images
        self.posiy = 0
        self.recorded_time = 0
        self.index = 0
        self.posi_list = [500 - 100,
                          1000 - 100,
                          1500 - 100,
                          2000 - 100,
                          2500 - 100,
                          3000 - 100,
                          3500 - 100,
                          4000 - 100
                          ]

        self.text1 = load('resources/MAIN STUFF/t1.png')
        self.text2 = load('resources/MAIN STUFF/t2.png')
        self.text3 = load('resources/MAIN STUFF/t3.png')
        self.text4 = load('resources/MAIN STUFF/t4.png')
        self.text5 = load('resources/MAIN STUFF/t5.png')
        self.text6 = load('resources/MAIN STUFF/t6.png')
        self.text7 = load('resources/MAIN STUFF/t7.png')
        self.text8 = load('resources/MAIN STUFF/t8.png')

    def start_main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Sound('resources/audio/mute vlick.wav').play()
                        self.start_at_first_time()

                    if event.key == pygame.K_m:
                        self.is_muted = not self.is_muted
                        Sound('resources/audio/mute vlick.wav').play()

            screen.blit(self.none, (0, 0))
            if self.is_muted:
                screen.blit(self.music_img_no, (screenWidth - 39, 5))
            else:
                screen.blit(self.music_img, (screenWidth - 39, 5))

            pygame.display.update()
            clock.tick(FPS)

    def controls(self, event):
        global recorded_time

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                recorded_time = pygame.time.get_ticks()
                # Officer.cop_img = load('resources/cop fly.png')
                Officer.jump()

            elif event.key == pygame.K_RIGHT:
                Officer.cop_Movementx += Officer.cop_speed

            elif event.key == pygame.K_LEFT:
                Officer.cop_Movementx -= Officer.cop_speed + 2

            elif event.key == pygame.K_SPACE:
                if Officer.player_score >= neededScore_to_Fire:
                    if not (Officer.bulletNum <= 0):
                        Officer.bullet_isFired = True
                        Officer.bullet.midleft = Officer.cop_rect.midright
                        Officer.bulletNum -= 1 / Officer.no_Of_Bullets_In_1_Pack
                        Sound('resources/audio/shoot.wav').play()
                    else:
                        Sound('resources/audio/empty gun.wav').play()

            if event.key == pygame.K_m:
                self.is_muted = not self.is_muted
                Sound('resources/audio/mute vlick.wav').play()

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_RIGHT:
                Officer.cop_Movementx -= Officer.cop_speed

            elif event.key == pygame.K_LEFT:
                Officer.cop_Movementx += Officer.cop_speed + 2

    def move_text(self):
        for i in range(len(self.posi_list)):
            self.posi_list[i] -= 1

    def start_at_first_time(self):
        if open('data/isfirst.txt').read() == 'yes':
            self.recorded_time = pygame.time.get_ticks()

            open('data/isfirst.txt', 'w').write('no')

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        gameLoop()

                self.move_text()

                if self.posi_list[7] <= -15:
                    gameLoop()

                screen.fill((0, 0, 0))

                screen.blit(self.text1, (100, self.posi_list[0]))
                screen.blit(self.text2, (100, self.posi_list[1]))
                screen.blit(self.text3, (100, self.posi_list[2]))
                screen.blit(self.text4, (100, self.posi_list[3]))
                screen.blit(self.text5, (100, self.posi_list[4]))
                screen.blit(self.text6, (100, self.posi_list[5]))
                screen.blit(self.text7, (100, self.posi_list[6]))
                screen.blit(self.text8, (100, self.posi_list[7]))

                pygame.display.update()
                clock.tick(FPS)

        else:
            gameLoop()


class GUNS:
    def __init__(self):
        self.heart_potion_img = load('resources/heart potion.png').convert_alpha()
        self.gun_img = load('resources/ammos.png').convert_alpha()
        self.fruit_img = load('resources/ammos.png').convert_alpha()
        self.gravityN = 0.30
        self.fruit_movement = 0

        self.fruit_rect = Rect(screenWidth + 20, 50, 35, 35)
        self.isAllowed_to_draw = False

        self.fruit_img = scale(self.fruit_img, (self.fruit_rect.w, self.fruit_rect.h))
        self.gun_img = scale(self.gun_img, (self.fruit_rect.w, self.fruit_rect.h))
        self.heart_potion_img = scale(self.heart_potion_img, (self.fruit_rect.w, self.fruit_rect.h))

    def randomize(self):
        self.isAllowed_to_draw = random.choice([False, True])
        self.fruit_img = random.choice([self.gun_img, self.gun_img, self.gun_img, self.heart_potion_img])

    def fruit_Movement(self):
        self.fruit_rect.x -= 7

    def fruit_gravity(self):
        self.fruit_movement += self.gravityN
        self.fruit_rect.centery += self.fruit_movement

    def check_collision(self, pipes):
        if self.fruit_rect.y <= 0:
            self.fruit_rect.y = 0
            self.isAllowed_to_draw = False

        elif self.fruit_rect.y >= screenHeight:
            self.fruit_rect.y = screenHeight

        elif self.fruit_rect.x <= 0:
            self.fruit_rect = Rect(screenWidth + 20, 50, 30, 30)
            self.isAllowed_to_draw = False

        for pipi in pipes:
            if self.fruit_rect.colliderect(pipi):
                if abs(self.fruit_rect.bottom - pipi.top) < 15:
                    self.fruit_rect.bottom = pipi.top
                    self.fruit_movement = 0

                elif abs(self.fruit_rect.top - pipi.bottom) < 15:
                    self.fruit_rect.top = pipi.bottom
                    self.fruit_movement = 0

        if self.fruit_rect.colliderect(floor):
            if (self.fruit_rect.bottom - floor.top) < 25:
                self.fruit_rect.bottom = floor.top
                self.fruit_movement = 0

        elif self.fruit_rect.colliderect(Officer.cop_rect):
            if self.fruit_img == self.gun_img:
                Officer.bulletNum = 5
            elif self.fruit_img == self.heart_potion_img:
                Officer.heartNum = 3
            else:
                Officer.heartNum = 3
                Officer.bulletNum = 5

            self.fruit_rect = Rect(screenWidth + 20, 50, 30, 30)
            self.isAllowed_to_draw = False

    def draw_fruit(self):
        if self.isAllowed_to_draw:
            screen.blit(self.fruit_img, self.fruit_rect)


# Variables
FPS = 60
neededScore_to_Fire = 25
recorded_time = 0
current_time = 0
JOKES = ['Good Job!',
         'Want a donut, Cop',
         '! Singham !',
         "Real Cop Will Go burrrr",
         'How was the jet pack',
         '''Master I found the 'Special cop' that you wanted''',
         'Well played',
         'You did it!']

# Classes
Main = MAIN()
Officer = OFFICER()
Plat = PLATFORM()
Enemy = ENEMY()
Coin = COINS()
Guns = GUNS()

# Setting up screen and clock
pygame.display.set_caption("Special Cops")
clock = pygame.time.Clock()

# lists
plat_list = []
enemy_list = []
coin_list = []

# Rect's
bg = pygame.image.load('resources/bg2.png').convert_alpha()
bg = pygame.transform.scale(bg, (screenWidth, screenHeight)).convert_alpha()
Bird_rect = pygame.Rect(150, screenHeight / 2, 33, 23)
floor = pygame.Rect(0, 500, screenWidth, 100)

# Images
f_img = scale(load('resources/asdn.png').convert_alpha(), (floor.w, floor.h + 50))

heart_full = load('resources/heart full.png').convert_alpha()
heart_half = load('resources/heart half.png').convert_alpha()
heart_no = load('resources/no heart.png').convert_alpha()

# Setting USEREVENTS
SPAWNPIPE = pygame.USEREVENT + 0
pygame.time.set_timer(SPAWNPIPE, 2500)

SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 2500)

SPAWN_FRUIT = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_FRUIT, 5000)

ENEMY_WAVE = pygame.USEREVENT + 3
pygame.time.set_timer(ENEMY_WAVE, 10 * 1000)

pygame.display.set_icon(load('resources/MAIN STUFF/batch.png'))


def find_highscore():
    arested_list = []
    bag_list = []

    largest_arrest = 0
    largest_bag_collected = 0

    with open('data/Scores.txt') as f:
        for line in f:
            data = line[34:].replace(' bags', '').split(' enemies and collected ')
            arrested, bags = int(data[0]), int(data[1])

            arested_list.append(arrested)
            bag_list.append(bags)

        for x in range(0, len(arested_list)):
            if arested_list[x] > largest_arrest:
                largest_arrest = arested_list[x]

        for x in range(0, len(bag_list)):
            if bag_list[x] > largest_bag_collected:
                largest_bag_collected = bag_list[x]

        f.close()

        return largest_arrest, largest_bag_collected


def restartPage():
    Officer.endgame()
    is_OnYes = None
    yes_R = pygame.Rect(30, 513, 170, 67)
    exit_R = pygame.Rect(846, 512, 92, 67)

    arrest, bag = find_highscore()

    highscore = pygame.font.Font('Teko-Light.ttf', 75).render(
        f"Highscore: {arrest}/{bag}", False, (255, 255, 0))
    highscore = pygame.transform.rotozoom(highscore, 5, 1)

    highscore_rect = highscore.get_rect(center=[screenWidth / 2, 100])

    t2 = pygame.font.Font('Teko-Light.ttf', 75).render(f"Arrested: {Officer.enemy_killed_num}", False, (255, 255, 255))
    t_rect2 = t2.get_rect(center=[screenWidth / 2, screenHeight / 2])

    t3 = pygame.font.Font('Teko-Light.ttf', 50).render(f"Money Bags: {Officer.bag_collected}", False, (255, 255, 255))
    t_rect3 = t3.get_rect(center=[screenWidth / 2, t_rect2.bottom])

    t = pygame.font.Font('Teko-Light.ttf', 50).render(random.choice(JOKES), False, (255, 255, 255))
    t_rect = t.get_rect(center=[screenWidth / 2, t_rect3.bottom + 20])

    screen.blit(load('resources/restart page.png'), (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameLoop()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if is_OnYes is not None:
                        if is_OnYes is True:
                            gameLoop()
                        else:
                            pygame.quit()
                            sys.exit()

        mousePosix, mousePosiy = pygame.mouse.get_pos()

        if yes_R.x < mousePosix < yes_R.x + yes_R.w and yes_R.y < mousePosiy < yes_R.y + yes_R.h:
            is_OnYes = True
        elif exit_R.x < mousePosix < exit_R.x + exit_R.w and exit_R.y < mousePosiy < exit_R.y + exit_R.h:
            is_OnYes = False

        screen.blit(t, t_rect)
        screen.blit(t2, t_rect2)
        screen.blit(t3, t_rect3)
        screen.blit(highscore, highscore_rect)

        pygame.display.update()
        clock.tick(FPS)


def check_score():
    if Main.is_muted:
        pygame.mixer.pause()

    if not Main.is_muted:
        pygame.mixer.unpause()


def reset_all_data():
    global enemy_list, plat_list, coin_list, Main, Officer, Plat, Enemy, Coin, Guns

    Officer = OFFICER()

    plat_list = []
    enemy_list = []
    coin_list = []


def gameLoop():
    global enemy_list, plat_list, coin_list, Main, Officer, Plat, Enemy, \
        Coin, Guns, current_time
    reset_all_data()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Officer.endgame()

                pygame.quit()
                sys.exit()

            if event.type == SPAWNPIPE:
                plat_list.append(Plat.create_platform())

            Main.controls(event)

            if event.type == SPAWN_ENEMY:
                for i in range(Enemy.enemy_spawn_num):
                    enemy_list.append(Enemy.create_enemy(False))

            if event.type == SPAWN_FRUIT:
                Guns.randomize()

            if event.type == ENEMY_WAVE:
                Sound('resources/audio/enemy wave coming.mp3').play()
                for i in range(Enemy.enemy_wave_spawn_num):
                    enemy_list.append(Enemy.create_enemy(True))

        Plat.posix -= Plat.plat_speed - 3
        plat_list = Plat.move_plat(plat_list)
        enemy_list = Enemy.move_enemy(enemy_list)
        coin_list = Coin.move_coin(coin_list)

        check_score()

        current_time = pygame.time.get_ticks()

        Officer.timer(recorded_time, current_time, 500)

        # Officer Stuff
        Plat.move_bg()

        Officer.fire_bullet()
        Officer.gravity()

        Officer.check_collision(plat_list)
        Officer.bullet_checkCollisions(enemy_list)

        screen.blit(f_img, floor)
        Officer.draw_bullet()
        Enemy.gravity(enemy_list)

        if not Main.is_muted:
            screen.blit(Main.music_img, (screenWidth - 39, 5))
        else:
            screen.blit(Main.music_img_no, (screenWidth - 39, 5))

        if Guns.isAllowed_to_draw:
            Guns.fruit_Movement()
            Guns.fruit_gravity()
            Guns.check_collision(plat_list)

        # Enemy Stuff
        Plat.draw_plat(plat_list)
        Enemy.draw_enemy(enemy_list)
        Coin.draw_coin(coin_list)
        Officer.enemy_and_other_stuff_counter()

        Officer.draw_hearts()
        Officer.draw_ammo()
        Officer.draw_cop()

        Guns.draw_fruit()

        pygame.display.flip()
        clock.tick(FPS)


Main.start_main()
