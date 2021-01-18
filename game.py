import os
import sys
import pygame
import pytmx


pygame.init()
size = width, height = 960, 800
screen = pygame.display.set_mode(size)
gravity = 3
clock = pygame.time.Clock()
started = True
# 1 - фон, 2 - лестница, 3 - поверхность для ходьбы, 4 - земля

'''
to-do:
меню
возможно ещё уровень
'''

# взято из урока:


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    image = pygame.transform.scale(image, (64, 64))
    return image


def load_wave(name):
    fullname = os.path.join('waves', name)
    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        sys.exit()
    return fullname


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Правила игры:",
                  "Ходьба: стрелочки,",
                  "Прыжок: пробел,",
                  "Выстрел: ы / s",
                  "",
                  "нажмите любую клавишу для продолжения"]

    fon = pygame.Rect(0, 0, 960, 800)
    pygame.draw.rect(screen, (205, 92, 92), fon, 0)
    font = pygame.font.Font(None, 30)
    text_coord = 80
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def dead_screen():
    intro_text = ["Вы умерли",
                  "",
                  "нажмите любую клавишу для продолжения"]

    fon = pygame.Rect(0, 0, 960, 800)
    pygame.draw.rect(screen, (205, 92, 92), fon, 0)
    font = pygame.font.Font(None, 30)
    text_coord = 80
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                import main
                terminate()


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = self.image.get_rect()
        self.rect.x = 32
        self.rect.y = 15 * 32
        self.speedx = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.hor_able = True  # защита от хождения по воздуху
        self.isJump = True
        self.on_right = True

    def go_horizont(self, is_ground):
        self.speedx = 0
        if self.rect.x < 16:  # чтобы за экран не уходил
            self.rect.x = 16
        elif self.rect.x >= 960 - 64:
            lvl.now_lvl = 2
            self.rect.x = 32
            self.rect.y = 15 * 32

        if is_ground == 1:
            self.hor_able = True  # чтобы игрок не ходил по воздуху

        if is_ground in range(1, 4) and self.hor_able:
            # проверка на возможность идти
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.speedx = -3  # float не работает
            if key[pygame.K_RIGHT]:
                self.speedx = 3
        else:
            self.speedx = 0
        self.rect.x += self.speedx

    def go_up(self, is_ladder):
        self.speedx = 0
        # id лестницы = 2
        # чтобы за экран не уходил
        if self.rect.y < 0:
            self.rect.y = 10
        elif self.rect.y >= 512:
            self.rect.y = 512

        if is_ladder == 2 or lvl.get_tileid(player.get_pos_plr(1)) == 2:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                self.hor_able = False
                self.speedx = -3  # float не работает
            if key[pygame.K_DOWN] and lvl.get_tileid(player.get_pos_plr()) != 3:
                self.hor_able = True
                self.speedx = 3
        else:
            self.speedx = 0
            self.hor_able = True
        self.rect.y += self.speedx

    def jump(self):
        # прыжок
        # key = pygame.key.get_pressed()
        # if key[pygame.K_SPACE]:
        if self.isJump:
            time = 0
            self.isJump = False
            while time <= 20000:
                self.rect.y -= gravity * clock.tick()
                time += 1
            #self.isJump = True

    def fall(self, floor):
        # падение игрока
        if floor != 3 and floor != 4 and floor != 2:
            self.rect = self.rect.move(0, 2)

    def get_pos_plr(self, plus=2):
        return self.rect.x // 32 + 1, self.rect.y // 32 + plus

    def die(self):
        # смерть игрока наступает если перескаются спрайты врага и игрока
        if pygame.sprite.collide_mask(enemy, player) and enemy.alive():
            print('dead')
            player.kill()
        if pygame.sprite.collide_mask(enemy2, player) and enemy2.alive():
            player.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.images = []

        for i in range(1, 9):
            self.images.append(load_image(f'fly_demon{i}.png'))
            self.images.append(load_image(f'fly_demon{i}.png'))

        self.index = 0
        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image, (96, 96))
        self.rect = self.image.get_rect()
        self.up = False
        self.enm_mask = pygame.mask.from_surface(self.image)

    def place(self, x_pos, y_pos):
        self.rect.x = x_pos * 32
        self.rect.y = y_pos * 32
        self.x = x_pos  # координаты в тайлах
        self.y = y_pos  # координаты в тайлах


    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def fly(self):
        speed = 0
        if self.rect.y >= (self.y - 3) * 32 and self.up:
            speed -= 2
            if self.rect.y == (self.y - 3) * 32:
                self.up = False

        else:
            speed += 2
            if self.rect.y == self.y * 32:
                self.up = True
        self.rect.y += speed


class Bullet(pygame.sprite.Sprite):
    # пуля/ выстрел, чтобы убивать врагов
    image = load_image("bullet.png")

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = self.image.get_rect()
        self.is_fire = False
        self.go_straight = 0  # чтобы пуля не поворачивалась за игроком
        if not self.is_fire:
            self.rect.x = player.rect.x + 1
            self.rect.y = player.rect.y + 2

        self.image = pygame.transform.scale(self.image, (10, 6))
        self.b_mask = pygame.mask.from_surface(self.image)

    def shoot(self):
        print('shooted')
        if not self.is_fire and not bullet.alive():
            self.rect.x = player.rect.x + 1
            self.rect.y = player.rect.y + 2

        elif pygame.sprite.collide_mask(enemy, bullet) and self.is_fire and enemy.alive():
            bullet.kill()
            enemy.kill()
            self.go_straight = 0
            print('killed')
            self.is_fire = False

        elif pygame.sprite.collide_mask(enemy2, bullet) and self.is_fire and enemy2.alive():
            bullet.kill()
            enemy2.kill()
            self.go_straight = 0
            print('killed')
            self.is_fire = False

        elif self.rect.x >= 981 or self.rect.x <= 0:
            bullet.kill()
            self.go_straight = 0
            self.is_fire = False

        elif self.is_fire and bullet.alive():
            if not self.go_straight:
                # таким образом проверка направления только один раз
                if player.on_right:
                    self.rect = self.rect.move(10, 0)
                    self.right = True
                    self.go_straight += 1
                else:
                    self.rect = self.rect.move(-10, 0)
                    self.right = False
                    self.go_straight += 1
            else:
                if self.right:
                    self.rect = self.rect.move(10, 0)
                else:
                    self.rect = self.rect.move(-10, 0)

    def update(self, plr_x, plr_y):
        self.rect.x = plr_x + 1
        self.rect.y = plr_y + 2



class Level:
    def __init__(self, num=1):
        self.map = pytmx.load_pygame(f"data/map{num}.tmx")
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = 32
        self.now_lvl = num

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tileid(self, pos):
        # print(self.map.get_tile_gid(pos[0], pos[1], 0))
        return self.map.get_tile_gid(pos[0], pos[1], 0)

    def new_lvl(self):
        lvl = Level(2)


running = True

FPS = 60

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(load_wave('main.mp3'))

start_screen()
all_sprites = pygame.sprite.Group()
player = Player(all_sprites)
bullet = Bullet()
bullet.kill()

enemy = Enemy(all_sprites)
enemy.place(12, 15)

enemy2 = Enemy(all_sprites)
enemy2.place(14, 4)

all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(enemy2)

lvl = Level(1)
lvl2 = Level(2)
pygame.mixer.music.play(-1)

while running:
    again = False
    clock.tick(FPS)
    if lvl.now_lvl == 1:
        lvl.render()
    else:
        lvl2.render()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN:
            started = False
            if event.key == pygame.K_LEFT and player.on_right:
                # поворот игрока в сторону движения
                player.image = pygame.transform.flip(player.image, True, False)
                player.on_right = False
            if event.key == pygame.K_RIGHT and not player.on_right:
                # поворот игрока в сторону движения
                player.image = pygame.transform.flip(player.image, True, False)
                player.on_right = True
            if event.key == pygame.K_s and not bullet.alive():
                bullet.is_fire = True

            if event.key == pygame.K_SPACE and not player.isJump:
                player.isJump = True
                player.jump()

    if player.alive():
        player.go_horizont(lvl.get_tileid(player.get_pos_plr()))
        player.go_up(lvl.get_tileid(player.get_pos_plr()))
        player.fall(lvl.get_tileid(player.get_pos_plr()))
        # от grt_pos_plr получаем место игрока (нижний middle) в теории
        # отдаем в get_tileid и в ответ получаем id клетки
        # отдаем это в go_up чтобы поднятся

        player.jump()
        player.die()
    else:
        dead_screen()

    # проверяет есть ли возможность выстрела
    if bullet.is_fire and bullet.alive():
        bullet.shoot()
    elif bullet.is_fire and not bullet.alive():
        all_sprites.add(bullet)
        bullet.shoot()
    elif not bullet.is_fire and not bullet.alive():
        bullet.update(player.rect.x, player.rect.y)

    enemy.update()
    enemy.fly()
    enemy2.update()
    enemy2.fly()

    all_sprites.draw(screen)
    pygame.display.flip()
    screen.fill((0, 0, 0))

