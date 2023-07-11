import keyboard

def on_key_event(event):
    # Suppress the keyboard event so it doesn't reach the game
    event.stop()

# Hook the keyboard event listener
keyboard.hook(on_key_event)

# Run your game loop here
while True:
    # Game logic goes here
    pass