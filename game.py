from script import create_enemies


try:
    try:
        from browser import document, alert # type: ignore
    except ImportError:
        document = None
        alert = lambda msg: print(f"ALERT: {msg}")
except ImportError:
    print("The 'browser' module is not available. This code must be run in a Brython environment.")
    document = None
    alert = lambda msg: print(f"ALERT: {msg}")

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
