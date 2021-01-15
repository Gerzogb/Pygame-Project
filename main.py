import os
import sys
import pygame


pygame.init()
size = width, height = 480, 270
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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
    image1 = pygame.transform.scale(image, (200, 200))
    return image1


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = self.image.get_rect()
        self.speedx = 0

    def go_horizont(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -3 # ниже 1 не работает
        if keystate[pygame.K_RIGHT]:
            self.speedx = 3
        self.rect.x += self.speedx



running = True
clock = pygame.time.Clock()
FPS = 60

all_sprites = pygame.sprite.Group()
player = Player(all_sprites)
all_sprites.add(player)

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.go_horizont()
    all_sprites.draw(screen)
    pygame.display.flip()
    screen.fill((0, 0, 0))

