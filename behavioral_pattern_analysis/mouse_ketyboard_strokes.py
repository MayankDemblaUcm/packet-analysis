from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

user_interactions = {
    "mouse": [],
    "keyboard": []
}

# Capture mouse movements
def on_move(x, y):
    user_interactions["mouse"].append(("move", x, y))

def on_click(x, y, button, pressed):
    user_interactions["mouse"].append(("click", button, pressed, x, y))

# Capture keyboard events
def on_press(key):
    user_interactions["keyboard"].append(("press", key))

def on_release(key):
    user_interactions["keyboard"].append(("release", key))

# Start listeners
with MouseListener(on_move=on_move, on_click=on_click) as mouse_listener, \
     KeyboardListener(on_press=on_press, on_release=on_release) as keyboard_listener:
    mouse_listener.join()
    keyboard_listener.join()

# Print the captured interactions
print(user_interactions)
