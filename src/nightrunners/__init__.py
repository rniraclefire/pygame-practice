import math
import pygame
import random
from typing import List

PIXELS_PER_UNIT = 64
ARENA_SIDE_LENGTH = PIXELS_PER_UNIT * 24
ARENA_BOUNDS = pygame.Rect(0, 0, 16, 16)

class Enemy:
    position: pygame.Vector2
    color: pygame.Color

def main():
    pygame.init()

    pygame.display.set_mode((480, 360))
    pygame.display.set_caption("NIGHTRUNNERS")

    display = pygame.display.get_surface()
    running = True

    player_position = pygame.Vector2(ARENA_BOUNDS.bottomright) / 2
    player_walkspeed = 5
    enemies: List[Enemy] = list()

    for _ in range(0, 64):
        enemy = Enemy()
        enemy.position = pygame.Vector2(random.uniform(ARENA_BOUNDS.left, ARENA_BOUNDS.right),
            random.uniform(ARENA_BOUNDS.top, ARENA_BOUNDS.bottom))
        enemy.color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        enemies.append(enemy)

    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(120) / 1000.0

        print(f"{math.floor(1.0 / dt) if dt > 0 else 0} FPS")

        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False
                break

        player_velocity = pygame.Vector2(0, 0)

        keys_pressed = pygame.key.get_pressed()
    
        move_direction = pygame.Vector2(0, 0)
        if keys_pressed[pygame.K_a]:
            move_direction.x -= 1
        if keys_pressed[pygame.K_d]:
            move_direction.x += 1
        if keys_pressed[pygame.K_w]:
            move_direction.y -= 1
        if keys_pressed[pygame.K_s]:
            move_direction.y += 1

        if move_direction.length_squared() > 0:
            player_velocity = move_direction.normalize() * player_walkspeed * dt
            player_position += player_velocity

        player_position.x = max(min(player_position.x, ARENA_BOUNDS.right), ARENA_BOUNDS.left)
        player_position.y = max(min(player_position.y, ARENA_BOUNDS.bottom), ARENA_BOUNDS.top)

        display_center = pygame.Vector2(display.get_width() / 2, display.get_height() / 2)
        def unit_to_display(unit_pos: pygame.Vector2) -> pygame.Vector2:
            return (
                display_center
                + (unit_pos - player_position) * PIXELS_PER_UNIT
            )

        display.fill((0, 0, 0))
        arena_top_left_screen = unit_to_display(
            pygame.Vector2(ARENA_BOUNDS.left, ARENA_BOUNDS.top)
        )
        arena_rect = pygame.Rect(
            arena_top_left_screen.x,
            arena_top_left_screen.y,
            ARENA_BOUNDS.width * PIXELS_PER_UNIT,
            ARENA_BOUNDS.height * PIXELS_PER_UNIT,
        )
        pygame.draw.rect(display, (64, 64, 64), arena_rect)

        for enemy in enemies:
            pygame.draw.circle(display, color=enemy.color, center=unit_to_display(enemy.position), radius=PIXELS_PER_UNIT * 0.125)

        pygame.draw.circle(display, color=(255, 255, 255), center=display_center, radius=PIXELS_PER_UNIT * 0.25)

        pygame.display.update()
    
    pygame.quit()

