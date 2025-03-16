from browser import document, alert

# Example game logic
def start_game(event):
    global lives, score, level, game_running, enemies, bullets, power_ups
    lives = 3
    score = 0
    level = 1
    game_running = True
    bullets = []
    power_ups = []
    create_enemies()
    alert("Game started!")

# Ensure the button is added dynamically to the DOM
document <= '<button id="start" style="position:absolute;top:10px;left:10px;">Start Game</button>'
document["start"].bind("click", start_game)
