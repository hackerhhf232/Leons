import pygame
import random
import math

pygame.init()

# =========================
# WINDOW & GLOBAL SETTINGS
# =========================
WIDTH, HEIGHT = 1000, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Mario Deluxe")

clock = pygame.time.Clock()
FPS = 60

# =========================
# COLORS
# =========================
SKY_TOP = (120, 190, 255)
SKY_BOTTOM = (190, 230, 255)
GROUND_GREEN = (95, 205, 120)
BRICK = (170, 90, 60)
PLAYER_RED = (225, 70, 70)
ENEMY_PURPLE = (140, 70, 160)
COIN_GOLD = (255, 215, 0)
UI_BG = (0, 0, 0, 120)
WHITE = (255, 255, 255)
BLACK = (25, 25, 25)

font = pygame.font.SysFont("consolas", 22)
big_font = pygame.font.SysFont("consolas", 42)

# =========================
# GAME STATES
# =========================
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"
WIN = "win"

game_state = MENU

# =========================
# PLAYER CLASS
# =========================
class Player:
    def __init__(self):
        self.rect = pygame.Rect(80, 380, 40, 55)
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -16
        self.gravity = 0.8
        self.on_ground = False
        self.lives = 3
        self.score = 0

    def move(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

    def draw(self):
        pygame.draw.rect(screen, PLAYER_RED, self.rect, border_radius=8)

# =========================
# ENEMY CLASS
# =========================
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.direction = random.choice([-1, 1])
        self.speed = 2

    def update(self):
        self.rect.x += self.direction * self.speed
        if random.randint(0, 100) == 0:
            self.direction *= -1

    def draw(self):
        pygame.draw.rect(screen, ENEMY_PURPLE, self.rect, border_radius=6)

# =========================
# PLATFORM CLASS
# =========================
class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(screen, GROUND_GREEN, self.rect)
        pygame.draw.rect(screen, BRICK, self.rect, 3)

# =========================
# COIN CLASS
# =========================
class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 18, 18)
        self.bounce = 0

    def draw(self):
        offset = int(math.sin(self.bounce) * 3)
        pygame.draw.circle(screen, COIN_GOLD,
                           (self.rect.centerx, self.rect.centery + offset), 9)
        self.bounce += 0.1

# =========================
# BACKGROUND
# =========================
clouds = [[random.randint(0, WIDTH), random.randint(60, 220)] for _ in range(7)]

def draw_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = SKY_TOP[0] * (1 - ratio) + SKY_BOTTOM[0] * ratio
        g = SKY_TOP[1] * (1 - ratio) + SKY_BOTTOM[1] * ratio
        b = SKY_TOP[2] * (1 - ratio) + SKY_BOTTOM[2] * ratio
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (WIDTH, y))

    for cloud in clouds:
        pygame.draw.circle(screen, WHITE, (cloud[0], cloud[1]), 20)
        pygame.draw.circle(screen, WHITE, (cloud[0] + 20, cloud[1] + 10), 18)
        pygame.draw.circle(screen, WHITE, (cloud[0] - 20, cloud[1] + 10), 18)
        cloud[0] -= 0.4
        if cloud[0] < -60:
            cloud[0] = WIDTH + 60

# =========================
# UI
# =========================
def draw_hud(player):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, 40))
    screen.blit(font.render(f"❤ Lives: {player.lives}", True, WHITE), (20, 10))
    screen.blit(font.render(f"★ Score: {player.score}", True, WHITE), (200, 10))
    screen.blit(font.render("ESC: Pause", True, WHITE), (WIDTH - 160, 10))

def center_text(text, y):
    t = big_font.render(text, True, WHITE)
    screen.blit(t, (WIDTH // 2 - t.get_width() // 2, y))

# =========================
# LEVEL SETUP
# =========================
player = Player()

platforms = [
    Platform(0, 450, 1000, 100),
    Platform(200, 360, 140, 25),
    Platform(420, 300, 140, 25),
    Platform(650, 240, 140, 25),
]

coins = [
    Coin(230, 330),
    Coin(450, 270),
    Coin(680, 210),
]

enemies = [
    Enemy(300, 410),
    Enemy(600, 410),
]

# =========================
# MAIN LOOP
# =========================
running = True
while running:
    clock.tick(FPS)
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == PLAYING:
                    game_state = PAUSED
                elif game_state == PAUSED:
                    game_state = PLAYING
            if event.key == pygame.K_RETURN and game_state == MENU:
                game_state = PLAYING

    keys = pygame.key.get_pressed()

    if game_state == MENU:
        center_text("MINI MARIO DELUXE", 180)
        center_text("Press ENTER to Start", 260)

    elif game_state == PAUSED:
        center_text("PAUSED", 200)
        center_text("Press ESC to Resume", 260)

    elif game_state == GAME_OVER:
        center_text("GAME OVER", 200)
        center_text("Close window to exit", 260)

    elif game_state == WIN:
        center_text("YOU WIN!", 200)
        center_text("Well played 🎉", 260)

    elif game_state == PLAYING:
        player.move(keys)
        player.apply_gravity()

        # Platform collision
        player.on_ground = False
        for p in platforms:
            if player.rect.colliderect(p.rect) and player.vel_y > 0:
                player.rect.bottom = p.rect.top
                player.vel_y = 0
                player.on_ground = True

        # Enemy logic
        for enemy in enemies:
            enemy.update()
            if player.rect.colliderect(enemy.rect):
                player.lives -= 1
                player.rect.topleft = (80, 380)
                if player.lives <= 0:
                    game_state = GAME_OVER

        # Coin collection
        for coin in coins[:]:
            if player.rect.colliderect(coin.rect):
                coins.remove(coin)
                player.score += 10

        if not coins:
            game_state = WIN

        # Draw world
        for p in platforms:
            p.draw()
        for coin in coins:
            coin.draw()
        for enemy in enemies:
            enemy.draw()
        player.draw()
        draw_hud(player)

    pygame.display.flip()

pygame.quit()
