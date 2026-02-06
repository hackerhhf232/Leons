import pygame
import random

pygame.init()

# Window
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Mario – Polished UI")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 22)

# Colors
SKY_TOP = (120, 190, 255)
SKY_BOTTOM = (180, 225, 255)
GROUND_GREEN = (90, 200, 120)
BRICK = (170, 90, 60)
PLAYER_RED = (220, 60, 60)
COIN_YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)

# Player
player = pygame.Rect(80, 350, 40, 50)
speed = 5
jump_power = -16
gravity = 0.8
velocity_y = 0
on_ground = False
lives = 3
score = 0

# Platforms
platforms = [
    pygame.Rect(0, 430, 900, 70),
    pygame.Rect(200, 340, 120, 25),
    pygame.Rect(400, 280, 120, 25),
    pygame.Rect(600, 220, 120, 25),
]

# Coins
coins = []
for p in platforms[1:]:
    coins.append(pygame.Rect(p.centerx - 10, p.y - 25, 20, 20))

# Background clouds
clouds = [[random.randint(0, WIDTH), random.randint(50, 200)] for _ in range(5)]

win = False


def draw_sky():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = SKY_TOP[0] * (1 - ratio) + SKY_BOTTOM[0] * ratio
        g = SKY_TOP[1] * (1 - ratio) + SKY_BOTTOM[1] * ratio
        b = SKY_TOP[2] * (1 - ratio) + SKY_BOTTOM[2] * ratio
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (WIDTH, y))


def draw_cloud(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), 20)
    pygame.draw.circle(screen, WHITE, (x + 20, y + 10), 18)
    pygame.draw.circle(screen, WHITE, (x - 20, y + 10), 18)


def draw_ui():
    lives_text = font.render(f"❤ Lives: {lives}", True, BLACK)
    score_text = font.render(f"★ Score: {score}", True, BLACK)
    screen.blit(lives_text, (20, 15))
    screen.blit(score_text, (WIDTH - 160, 15))


running = True
while running:
    clock.tick(60)

    draw_sky()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not win and lives > 0:
        # Movement
        if keys[pygame.K_a]:
            player.x -= speed
        if keys[pygame.K_d]:
            player.x += speed

        # Jump
        if keys[pygame.K_SPACE] and on_ground:
            velocity_y = jump_power
            on_ground = False

        # Gravity
        velocity_y += gravity
        player.y += velocity_y

        # Platform collision
        on_ground = False
        for platform in platforms:
            if player.colliderect(platform) and velocity_y > 0:
                player.bottom = platform.top
                velocity_y = 0
                on_ground = True

        # Collect coins
        for coin in coins[:]:
            if player.colliderect(coin):
                coins.remove(coin)
                score += 10

        if len(coins) == 0:
            win = True

        # Screen bounds
        player.x = max(0, min(WIDTH - player.width, player.x))

    # Clouds
    for cloud in clouds:
        draw_cloud(cloud[0], cloud[1])
        cloud[0] -= 0.3
        if cloud[0] < -60:
            cloud[0] = WIDTH + 60

    # Platforms
    for platform in platforms:
        pygame.draw.rect(screen, GROUND_GREEN, platform)
        pygame.draw.rect(screen, BRICK, platform, 3)

    # Coins
    for coin in coins:
        pygame.draw.circle(screen, COIN_YELLOW, coin.center, 10)

    # Player
    pygame.draw.rect(screen, PLAYER_RED, player, border_radius=6)

    draw_ui()

    if win:
        text = font.render("YOU WIN! 🎉", True, BLACK)
        screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
