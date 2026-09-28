import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Candle Burning")

# Colors
CANDLE_COLOR = (240, 220, 200)
WAX_SHADE = (220, 200, 180)
FLAME_GRADIENT = [(255, 165, 0), (255, 140, 0), (255, 215, 0), (255, 69, 0)]

clock = pygame.time.Clock()

def draw_candle():
    # Candle body with rounded top and bottom
    center_x = WIDTH // 2
    top_y = HEIGHT // 2

    # Candle body
    pygame.draw.rect(screen, CANDLE_COLOR, (center_x - 20, top_y, 40, 150))

    # Rounded top (ellipse)
    pygame.draw.ellipse(screen, CANDLE_COLOR, (center_x - 20, top_y - 10, 40, 20))

    # Rounded base (ellipse)
    pygame.draw.ellipse(screen, WAX_SHADE, (center_x - 20, top_y + 140, 40, 20))

def draw_flame():
    # Teardrop flame: ellipse + triangle
    center_x = WIDTH // 2
    base_y = HEIGHT // 2 - 10

    flicker_offset = random.randint(-4, 4)

    # Flame base (rounded ellipse)
    flame_base_color = random.choice(FLAME_GRADIENT)
    pygame.draw.ellipse(screen, flame_base_color, (center_x - 6, base_y - 10 + flicker_offset, 12, 14))

    # Flame top (pointed tip like triangle)
    tip_color = random.choice(FLAME_GRADIENT)
    flame_tip = [
        (center_x, base_y - 30 + flicker_offset),   # Top point
        (center_x - 6, base_y + flicker_offset),    # Bottom left
        (center_x + 6, base_y + flicker_offset)     # Bottom right
    ]
    pygame.draw.polygon(screen, tip_color, flame_tip)

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Night background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_candle()
    draw_flame()

    pygame.display.flip()
    clock.tick(12)  # Control flicker speed

pygame.quit()
sys.exit()
