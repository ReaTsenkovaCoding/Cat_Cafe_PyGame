import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1920, 1080), pygame.SCALED)
pygame.display.set_caption("Scale Test")

# Load player sprite - adjust path if needed
player = pygame.image.load("assets/player.png").convert_alpha()
player = pygame.transform.scale(player, (192, 192))

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((100, 100, 120))  # placeholder background color

    # Draw player center screen
    screen.blit(player, (1920//2 - 64, 1080//2 - 64))

    pygame.display.flip()
    clock.tick(60)