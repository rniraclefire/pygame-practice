import sys

import pygame

pygame.init()

clock = pygame.time.Clock()
window = pygame.display.set_mode(
    (480, 320),
)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
