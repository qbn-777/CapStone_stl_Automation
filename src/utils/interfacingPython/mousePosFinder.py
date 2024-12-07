import pyautogui
import time

print("Move your mouse to the desired position. The coordinates will be displayed every second.")
try:
    while True:
        x, y = pyautogui.position()
        print(f"X: {x}, Y: {y}")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nProgram terminated.")
