import pygame
from game import load_image, end_screen, start_screen, Game


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = self.image.get_rect()
        self.rect.x = 32
        self.rect.y = 15 * 32
        self.speedx = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.isJump = True
        self.on_right = True
        self.KILLS = 0  # счетчик убийств, от к-го зависит концовка
        self.can_fall = True

    def go_horizont(self, is_ground):
        self.speedx = 0
        if self.rect.x < 16:  # чтобы за экран не уходил
            self.rect.x = 16
        elif self.rect.x >= 960 - 64:
            if Game.lvl.now_lvl == 1:
                Game.lvl.now_lvl = 2
                self.rect.x = 32
                self.rect.y = 15 * 32
            elif Game.lvl.now_lvl == 2:
                Game.lvl.now_lvl = 3
                self.rect.x = 32
                self.rect.y = 15 * 32
            elif Game.lvl.now_lvl == 3:
                Game.lvl.now_lvl = 4
                self.rect.x = 32
                self.rect.y = 15 * 32
            elif Game.lvl.now_lvl == 4:
                end_screen()

        if is_ground in range(1, 4):
            # проверка на возможность идти
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.speedx = -4  # float не работает
            if key[pygame.K_RIGHT]:
                self.speedx = 4
        else:
            self.speedx = 0
        self.rect.x += self.speedx

    def go_up(self, is_ladder):
        self.speedx = 0
        # id лестницы = 2
        # чтобы за экран не уходил
        if self.rect.y < 0:
            self.rect.y = 10
        elif self.rect.y > 700:
            Game.player.kill()

        if is_ladder == 2 or Game.lvl.get_tileid(Game.player.get_pos_plr(1)) == 2:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                self.speedx = -3  # float не работает
            if key[pygame.K_DOWN] and Game.lvl.get_tileid(Game.player.get_pos_plr()) != 3:
                self.speedx = 3
        else:
            self.speedx = 0
        self.rect.y += self.speedx

    def jump(self):
        # прыжок
        # key = pygame.key.get_pressed()
        # if key[pygame.K_SPACE]:
        if self.isJump:
            time = 0
            self.isJump = False
            while time <= 20000:
                self.rect.y -= Game.GRAVITY * Game.clock.tick()
                time += 1
            # self.isJump = True

    def fall(self, floor):
        # падение игрока
        if self.can_fall:
            if floor != 3 and floor != 4 and floor != 2:
                self.rect = self.rect.move(0, 3)

    def get_pos_plr(self, plus=1):
        return self.rect.x // 32 + 1, self.rect.y // 32 + plus

    def die(self):
        # смерть игрока наступает если перескаются спрайты врага и игрока
        if pygame.sprite.collide_mask(Game.enemy, Game.player) and Game.enemy.alive():
            print('dead')
            Game.player.kill()
        if pygame.sprite.collide_mask(Game.enemy2, Game.player) and Game.enemy2.alive():
            Game.player.kill()
        if pygame.sprite.collide_mask(Game.enemy3, Game.player) and Game.enemy3.alive():
            Game.player.kill()
        if pygame.sprite.collide_mask(Game.enemy4, Game.player) and Game.enemy4.alive():
            Game.player.kill()
        if self.rect.y > 700:
            Game.player.kill()
        if Game.lvl.get_tileid(Game.player.get_pos_plr()) == 3:
            Game.player.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.images = []

        for i in range(1, 9):
            self.images.append(load_image(f'fly_demon{i}.png'))
            self.images.append(load_image(f'fly_demon{i}.png'))
            # два раза одно и то же, ибо кадров мало, а иначе слишком быстро

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


class Platform(pygame.sprite.Sprite):
    image = load_image("platform.png")

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = self.image.get_rect()
        self.rect.y = 17 * 32
        self.rect.x = 21 * 32
        self.start = self.rect.x
        self.image = pygame.transform.scale(self.image, (64, 32))
        self.p_mask = pygame.mask.from_surface(self.image)
        self.go_right = False

    def fly_platform(self):
        if self.go_right:
            self.rect = self.rect.move(2, 0)
        else:
            self.rect = self.rect.move(-2, 0)
        if self.rect.x == self.start + 416:
            self.go_right = False
        elif self.rect.x == self.start:
            self.go_right = True

        if pygame.sprite.collide_mask(Game.player, Game.platform):
            Game.player.can_fall = False
            Game.player.rect.y -= 1
        else:
            Game.player.can_fall = True

    def replace_platform(self, new_x, new_y):
        self.rect.x = new_x * 32
        self.start = new_x * 32
        self.rect.y = new_y * 32
        # координаты в тайлах



class Bullet(pygame.sprite.Sprite):
    # пуля/ выстрел, чтобы убивать врагов
    image = load_image("bullet.png")

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = self.image.get_rect()
        self.is_fire = False
        self.go_straight = 0  # чтобы пуля не поворачивалась за игроком
        if not self.is_fire:
            self.rect.x = Game.player.rect.x + 1
            self.rect.y = Game.player.rect.y + 2

        self.image = pygame.transform.scale(self.image, (10, 6))
        self.b_mask = pygame.mask.from_surface(self.image)

    def shoot(self):
        print('shooted')
        if not self.is_fire and not Game.bullet.alive():
            self.rect.x = Game.player.rect.x + 1
            self.rect.y = Game.player.rect.y + 2

        elif pygame.sprite.collide_mask(Game.enemy, Game.bullet) and self.is_fire and Game.enemy.alive():
            Game.bullet.kill()
            Game.enemy.kill()
            self.go_straight = 0
            Game.player.KILLS += 1
            print('killed')
            self.is_fire = False

        elif pygame.sprite.collide_mask(Game.enemy2, Game.bullet) and self.is_fire and Game.enemy2.alive():
            Game.bullet.kill()
            Game.enemy2.kill()
            self.go_straight = 0
            Game.player.KILLS += 1
            print('killed')
            self.is_fire = False

        elif pygame.sprite.collide_mask(Game.enemy3, Game.bullet) and self.is_fire and Game.enemy3.alive():
            Game.bullet.kill()
            Game.enemy3.kill()
            self.go_straight = 0
            Game.player.KILLS += 1
            print('killed')
            self.is_fire = False

        elif pygame.sprite.collide_mask(Game.enemy4, Game.bullet) and self.is_fire and Game.enemy4.alive():
            Game.bullet.kill()
            Game.enemy4.kill()
            self.go_straight = 0
            Game.player.KILLS += 1
            print('killed')
            self.is_fire = False

        elif self.rect.x >= 981 or self.rect.x <= 0:
            Game.bullet.kill()
            self.go_straight = 0
            self.is_fire = False

        elif self.is_fire and Game.bullet.alive():
            if not self.go_straight:
                # таким образом проверка направления только один раз
                if Game.player.on_right:
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
    def __init__(self, lvl=1):
        self.map = Game.pytmx.load_pygame(f"data/map{lvl}.tmx")
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = 32
        self.now_lvl = lvl

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                Game.SCREEN.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tileid(self, pos):
        # print(self.map.get_tile_gid(pos[0], pos[1], 0))
        return self.map.get_tile_gid(pos[0], pos[1], 0)