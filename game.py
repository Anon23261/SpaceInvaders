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

# Bind a button click to start the game
document <= '<button id="start">Start Game</button>'
document["start"].bind("click", start_game)
