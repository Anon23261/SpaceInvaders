from browser import document, html, timer
import random

# Canvas setup
canvas = document["gameCanvas"]
ctx = canvas.getContext("2d")

# Game variables
WIDTH, HEIGHT = 800, 600
player = {"x": WIDTH // 2, "y": HEIGHT - 50, "width": 50, "height": 30, "color": "green", "dx": 0}
bullets = []
enemies = []
score = 0
game_running = True

# Additional game variables
lives = 3
level = 1
power_ups = []

# Key handling
keys = set()

def key_down(event):
    keys.add(event.key)

def key_up(event):
    keys.discard(event.key)

document.bind("keydown", key_down)
document.bind("keyup", key_up)

# Game functions
def draw_player():
    ctx.fillStyle = player["color"]
    ctx.fillRect(player["x"], player["y"], player["width"], player["height"])

def move_player():
    if "ArrowRight" in keys:
        player["x"] += 5
    if "ArrowLeft" in keys:
        player["x"] -= 5
    player["x"] = max(0, min(WIDTH - player["width"], player["x"]))

def shoot_bullet():
    if " " in keys:
        bullets.append({"x": player["x"] + player["width"] // 2 - 2, "y": player["y"], "width": 4, "height": 10})

def draw_bullets():
    ctx.fillStyle = "yellow"
    for bullet in bullets:
        ctx.fillRect(bullet["x"], bullet["y"], bullet["width"], bullet["height"])

def update_bullets():
    global bullets
    bullets = [b for b in bullets if b["y"] > 0]
    for bullet in bullets:
        bullet["y"] -= 5

def create_enemies():
    global enemies
    enemies = [{"x": x * 60, "y": y * 40, "width": 40, "height": 20, "color": "red"} for y in range(3) for x in range(10)]

def draw_enemies():
    ctx.fillStyle = "red"
    for enemy in enemies:
        ctx.fillRect(enemy["x"], enemy["y"], enemy["width"], enemy["height"])

def detect_collisions():
    global bullets, enemies, score
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

def draw_score():
    ctx.fillStyle = "white"
    ctx.font = "20px Arial"
    ctx.fillText(f"Score: {score}", 10, 20)

def draw_lives():
    ctx.fillStyle = "white"
    ctx.font = "20px Arial"
    ctx.fillText(f"Lives: {lives}", WIDTH - 100, 20)

def draw_level():
    ctx.fillStyle = "white"
    ctx.font = "20px Arial"
    ctx.fillText(f"Level: {level}", WIDTH // 2 - 40, 20)

def create_power_up():
    power_ups.append({"x": random.randint(0, WIDTH - 20), "y": 0, "width": 20, "height": 20, "color": "blue", "type": "shield"})

def draw_power_ups():
    ctx.fillStyle = "blue"
    for power_up in power_ups:
        ctx.fillRect(power_up["x"], power_up["y"], power_up["width"], power_up["height"])

def update_power_ups():
    global power_ups, lives
    for power_up in power_ups[:]:
        power_up["y"] += 2
        if (player["x"] < power_up["x"] + power_up["width"] and
            player["x"] + player["width"] > power_up["x"] and
            player["y"] < power_up["y"] + power_up["height"] and
            player["y"] + player["height"] > power_up["y"]):
            power_ups.remove(power_up)
            if power_up["type"] == "shield":
                lives += 1

def check_game_over():
    global game_running
    if lives <= 0:
        game_running = False
        alert("Game Over! Your score: " + str(score))

def next_level():
    global level, enemies
    if not enemies:
        level += 1
        create_enemies()

def game_loop():
    if not game_running:
        return
    ctx.clearRect(0, 0, WIDTH, HEIGHT)
    move_player()
    shoot_bullet()
    update_bullets()
    update_power_ups()
    detect_collisions()
    draw_player()
    draw_bullets()
    draw_enemies()
    draw_power_ups()
    draw_score()
    draw_lives()
    draw_level()
    check_game_over()
    next_level()

# Ensure the game starts automatically when the page loads
def initialize_game():
    global lives, score, level, game_running, bullets, power_ups
    lives = 3
    score = 0
    level = 1
    game_running = True
    bullets = []
    power_ups = []
    create_enemies()

initialize_game()

# Initialize game
create_enemies()
timer.set_interval(game_loop, 16)  # 60 FPS

