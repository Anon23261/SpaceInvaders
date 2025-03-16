from browser import document, alert

# Example game logic
def start_game(event):
    alert("Game started!")

# Bind a button click to start the game
document <= '<button id="start">Start Game</button>'
document["start"].bind("click", start_game)
