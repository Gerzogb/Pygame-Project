import os
import sys
import pygame
import pytmx


pygame.init()
size = width, height = 960, 800
screen = pygame.display.set_mode(size)


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
    image = pygame.transform.scale(image, (32, 32))
    return image


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = self.image.get_rect()
        self.rect.x = 32
        self.rect.y = 16 * 32
        self.speedx = 0

    def go_horizont(self):
        self.speedx = 0
        if self.rect.x < 0: #чтобы за экран не уходил
            self.rect.x = 0
        elif self.rect.x > 928:
            self.rect.x = 928
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.speedx = -3 # float не работает
        if key[pygame.K_RIGHT]:
            self.speedx = 3
        self.rect.x += self.speedx


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

    def get_tileid(self):
        pass


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

    player.go_horizont()
    all_sprites.draw(screen)
    pygame.display.flip()
    screen.fill((0, 0, 0))

