from browser import document, html, timer

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

def game_loop():
    if not game_running:
        return
    ctx.clearRect(0, 0, WIDTH, HEIGHT)
    move_player()
    shoot_bullet()
    update_bullets()
    detect_collisions()
    draw_player()
    draw_bullets()
    draw_enemies()
    draw_score()

# Initialize game
create_enemies()
timer.set_interval(game_loop, 16)  # 60 FPS

