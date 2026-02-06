import pygame
import random
import math

pygame.init()

# Window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Arena")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 28)

# Colors
WHITE = (255, 255, 255)
RED = (220, 50, 50)
BLUE = (50, 150, 255)
BLACK = (20, 20, 20)

# Player
player_pos = [WIDTH // 2, HEIGHT // 2]
player_radius = 15
player_speed = 5

# Enemies
enemy_radius = 15
enemy_speed = 2
enemies = []

score = 0
game_over = False


def spawn_enemy():
    x = random.choice([0, WIDTH])
    y = random.randint(0, HEIGHT)
    enemies.append([x, y])


def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def draw_text(text, x, y, color=WHITE):
    screen.blit(font.render(text, True, color), (x, y))


spawn_timer = 0

# Main Loop
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # Player movement
        if keys[pygame.K_w]:
            player_pos[1] -= player_speed
        if keys[pygame.K_s]:
            player_pos[1] += player_speed
        if keys[pygame.K_a]:
            player_pos[0] -= player_speed
        if keys[pygame.K_d]:
            player_pos[0] += player_speed

        # Keep player inside screen
        player_pos[0] = max(player_radius, min(WIDTH - player_radius, player_pos[0]))
        player_pos[1] = max(player_radius, min(HEIGHT - player_radius, player_pos[1]))

        # Spawn enemies
        spawn_timer += 1
        if spawn_timer > 60:
            spawn_enemy()
            spawn_timer = 0
            score += 1
            enemy_speed += 0.05

        # Move enemies
        for enemy in enemies:
            angle = math.atan2(player_pos[1] - enemy[1], player_pos[0] - enemy[0])
            enemy[0] += math.cos(angle) * enemy_speed
            enemy[1] += math.sin(angle) * enemy_speed

            if distance(player_pos, enemy) < player_radius + enemy_radius:
                game_over = True

    # Draw player
    pygame.draw.circle(screen, BLUE, player_pos, player_radius)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.circle(screen, RED, enemy, enemy_radius)

    draw_text(f"Score: {score}", 10, 10)

    if game_over:
        draw_text("GAME OVER", WIDTH // 2 - 90, HEIGHT // 2 - 20, RED)
        draw_text("Press ESC to quit", WIDTH // 2 - 140, HEIGHT // 2 + 20)

        if keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()

pygame.quit()
