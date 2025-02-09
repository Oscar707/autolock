import pyautogui
import cv2
import numpy as np
import time

# Configuration
CONFIDENCE_THRESHOLD = 0.7
BAN = ""
PICK = ""



def get_center(needle, haystack):
    location = pyautogui.locate(needleImage=needle,haystackImage=haystack,confidence=CONFIDENCE_THRESHOLD,grayscale=True)
    if location:
        center = pyautogui.center(location)  
        print(f"found {needle} at x:{center[0]} y:{center[1]}")
        return center
    return None

def screenshot():
    im1 = pyautogui.screenshot('test.png')
    return im1
def move_click(location,y_offset):
    pyautogui.moveTo(location[0],location[1]+y_offset,duration=1, tween=pyautogui.easeInOutQuad)
    pyautogui.click()
    return 
def type(name):
    pyautogui.write(name,interval=0.1)
    return

def queue():
    try:
        screen = screenshot()
        accept = get_center('accept.png', screen) #location of accept
        move_click(accept,0)
    except Exception as e:
        print(f"An error occurred (queue phase): {e}")
    return
def pick(name):
    try:
        screen = screenshot()
        lock = get_center('lock_in.png', screen) #location of lock in button
        search = get_center('search.png',screen) #location of search bar
        ref = get_center('ref.png',screen) #location of ref icon
        move_click(search,0)
        type(name)
        move_click(ref,50)
        move_click(lock,0)
        
    except Exception as e:
        print(f"An error occurred (pick phase): {e}")
    return

def ban(name):
    try:
        screen = screenshot()
        ban = get_center('ban.png', screen) #location of ban button
        search = get_center('search.png',screen) #location of search bar
        ref = get_center('ref.png',screen)
        move_click(search,0)
        type(name)
        move_click(ref,50)
        move_click(ban,0)
        
    except Exception as e:
        print(f"An error occurred (ban phase): {e}")
    return

def get_current_phase(screenshot):
    # Helper function to check for images
    def check_image(image_name):
        return pyautogui.locate(
            needleImage=f"{image_name}.png",
            haystackImage=screenshot,
            confidence=0.5,
            grayscale=True
        ) is not None

    # Determine phase based on found images
    phase_indicators = (
        check_image("queue"),
        check_image("ban"),
        check_image("pick")
    )

    match phase_indicators:
        case (True, False, False):
            return "queue"
        case (False, True, False):
            return "ban"
        case (False, False, True):
            return "pick"
        case _:
            return "unknown"

def handle_phase(screenshot):
    current_phase = get_current_phase(screenshot)
    
    match current_phase:
        case "queue":
            print("In queue phase")
            queue()
        case "ban":
            print("In ban phase")
            ban("ekko")
        case "pick":
            print("In pick phase")
            pick("syndra")
        case "unknown":
            print("Could not determine phase")
            handle_unknown_phase

def handle_unknown_phase():
    # Handle cases where phase cannot be determined
    time.sleep(5)
    return main()

def main():
    pyautogui.hotkey('alt','tab')
    while True:
        try:
            screenshot = pyautogui.screenshot()
            handle_phase(screenshot)
            time.sleep(1)  # Add delay to prevent excessive CPU usage
        except KeyboardInterrupt:
            print("Script stopped by user")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript stopped by user.")