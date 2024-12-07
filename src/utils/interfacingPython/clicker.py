import pyautogui
import time

def click_on_screen(x, y, interval, duration):
    end_time = time.time() + duration
    count =0
    while time.time() < end_time:
        
        pyautogui.click(x=x, y=y)
        count+=1
        # print(count)

        if count % 30 == 0:
            pyautogui.click(x=1722, y=307)
            # print("Second cclick")
        time.sleep(interval)

# Example usage:
click_on_screen(1671, 536, 0.0000001, 40)
