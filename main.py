import os
import sys
import pygame
import pytmx


pygame.init()
size = width, height = 960, 800
screen = pygame.display.set_mode(size)
# 1 - фон, 2 - лестница, 3 - поверхность для ходьбы, 4 - земля

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


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = self.image.get_rect()
        self.rect.x = 32
        self.rect.y = 15 * 32
        self.speedx = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.hor_able = True

    def go_horizont(self, is_ground):
        self.speedx = 0
        if self.rect.x < 0:  # чтобы за экран не уходил
            self.rect.x = 0
        elif self.rect.x > 896:
            self.rect.x = 896

        if is_ground == 1:
            self.hor_able = True # чтобы игрок не ходил по воздуху

        if is_ground in range(1, 4) and self.hor_able:
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
        # if self.rect.x < 0:  # чтобы за экран не уходил
        #     self.rect.x = 0
        # elif self.rect.x > 512:
        #     self.rect.x = 512

        if (lvl.get_tileid(player.get_pos_plr()) - 1 == 2 or is_ladder == 2) or is_ladder != 3:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                self.hor_able = False
                self.speedx = -3  # float не работает
            if key[pygame.K_DOWN]:
                self.hor_able = False
                self.speedx = 3
        else:
            self.speedx = 0
            self.hor_able = True
        self.rect.y += self.speedx

    def fall(self, floor): # падение игрока
        if floor != 3 and floor != 4 and floor != 2:
            self.rect = self.rect.move(0, 2)


    def get_pos_plr(self):
        return self.rect.x // 32 + 1, self.rect.y // 32 + 2


class Level:
    def __init__(self):
        self.map = pytmx.load_pygame("data/map.tmx")
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = 32

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tileid(self, pos):
        print(self.map.get_tile_gid(pos[0], pos[1], 0))
        return self.map.get_tile_gid(pos[0], pos[1], 0)

running = True
clock = pygame.time.Clock()
FPS = 60

all_sprites = pygame.sprite.Group()
player = Player(all_sprites)
all_sprites.add(player)

lvl = Level()

while running:
    clock.tick(FPS)
    lvl.render()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.go_horizont(lvl.get_tileid(player.get_pos_plr()))
    player.go_up(lvl.get_tileid(player.get_pos_plr()))
    # от grt_pos_plr получаем место игрока (нижний middle) в теории
    # отдаем в get_tileid и в ответ получаем id клетки
    # отдаем это в go_up чтобы поднятся
    player.fall(lvl.get_tileid(player.get_pos_plr()))

    all_sprites.draw(screen)
    pygame.display.flip()
    screen.fill((0, 0, 0))

