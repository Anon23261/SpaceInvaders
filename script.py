import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player properties
player = {
    "x": WIDTH // 2,
    "y": HEIGHT - 50,
    "width": 50,
    "height": 30,
    "speed": 5,
    "dx": 0,
    "color": GREEN,
    "shielded": False,
    "armor": 0
}

# Enemy properties
enemies = []
enemy_speed = 1
enemy_width = 40
enemy_height = 20

# Bullet properties
bullets = []
bullet_speed = 7

# Enemy bullets
enemy_bullets = []
enemy_bullet_speed = 3

# Power-ups
power_ups = []
power_up_types = [
    {"type": "scoreBoost", "color": ORANGE, "effect": lambda: increase_score(50)},
    {"type": "speedBoost", "color": PURPLE, "effect": lambda: boost_speed()},
    {"type": "shield", "color": CYAN, "effect": lambda: activate_shield()},
    {"type": "armor", "color": BLUE, "effect": lambda: increase_armor()}
]

# Score and level
score = 0
current_level = 1
max_levels = 5

# Ship selection
ships = [
    {"speed": 5, "color": GREEN},
    {"speed": 7, "color": BLUE},
    {"speed": 4, "color": RED}
]
selected_ship = 0

# Game state
game_state = "start"

# Pause functionality
paused = False

def toggle_pause():
    global paused
    paused = not paused

def draw_pause_screen():
    font = pygame.font.Font(None, 72)
    pause_text = font.render("Paused", True, WHITE)
    screen.blit(pause_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

# Functions
def draw_player():
    pygame.draw.rect(screen, player["color"], (player["x"], player["y"], player["width"], player["height"]))

def move_player():
    player["x"] += player["dx"]
    if player["x"] < 0:
        player["x"] = 0
    elif player["x"] + player["width"] > WIDTH:
        player["x"] = WIDTH - player["width"]

def create_enemies(rows, cols):
    global enemies
    enemies = []
    for row in range(rows):
        for col in range(cols):
            enemies.append({
                "x": col * (enemy_width + 10),
                "y": row * (enemy_height + 10),
                "width": enemy_width,
                "height": enemy_height,
                "color": RED
            })

def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, enemy["color"], (enemy["x"], enemy["y"], enemy["width"], enemy["height"]))

def shoot_bullet():
    bullets.append({"x": player["x"] + player["width"] // 2, "y": player["y"], "width": 5, "height": 10})

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, (bullet["x"], bullet["y"], bullet["width"], bullet["height"]))

def update_bullets():
    global bullets
    bullets = [bullet for bullet in bullets if bullet["y"] > 0]
    for bullet in bullets:
        bullet["y"] -= bullet_speed

# Level progression
def next_level():
    global current_level, enemies, enemy_speed
    if current_level < max_levels:
        current_level += 1
        enemy_speed += 1
        create_enemies(3 + current_level, 8)
    else:
        win_game()

def win_game():
    global game_state
    game_state = "win"

def draw_win_screen():
    font = pygame.font.Font(None, 72)
    win_text = font.render("You Win!", True, WHITE)
    screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

# Update detect_collisions to handle level progression
def detect_collisions():
    global score, enemies
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if (bullet["x"] < enemy["x"] + enemy["width"] and
                bullet["x"] + bullet["width"] > enemy["x"] and
                bullet["y"] < enemy["y"] + enemy["height"] and
                bullet["y"] + bullet["height"] > enemy["y"]):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break
    if not enemies:
        next_level()

def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def start_game():
    global game_state, score, current_level
    score = 0
    current_level = 1
    create_enemies(3, 8)
    game_state = "playing"

def game_over():
    global game_state
    game_state = "over"

# Main game loop
def main():
    global game_state, paused
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player["dx"] = player["speed"]
                elif event.key == pygame.K_LEFT:
                    player["dx"] = -player["speed"]
                elif event.key == pygame.K_SPACE and game_state == "playing" and not paused:
                    shoot_bullet()
                elif event.key == pygame.K_p:
                    toggle_pause()
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    player["dx"] = 0

        if game_state == "start":
            start_game()
        elif game_state == "playing":
            if paused:
                draw_pause_screen()
            else:
                move_player()
                update_bullets()
                detect_collisions()
                draw_player()
                draw_enemies()
                draw_bullets()
                draw_score()
        elif game_state == "over":
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        elif game_state == "win":
            draw_win_screen()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
