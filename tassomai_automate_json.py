import pyautogui # controls the mouse and can take screenshots
import pytesseract # converts screenshot into text
import time # time
import re # idk
from PIL import Image
import numpy as np
import json # for database
import random

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

json_file = 'questions.json'
wrong_colour = "#DC4242"
right_colour = "#85C24A"

# the different positions for clicking answers
def top_right():
    pyautogui.moveTo(1320, 640)
def top_left():
    pyautogui.moveTo(750, 640)
def bottom_right():
    pyautogui.moveTo(1320, 890)
def bottom_left():
    pyautogui.moveTo(750, 890)
def click():
    pyautogui.click()

# enter the quiz
def start_questions(t):
    time.sleep(0.5)
    if t == 1:
        pyautogui.moveTo(1400, 800) # task1
    else:
        pyautogui.moveTo(1400, 985) # task2
    click()
    time.sleep(4.5)
    pyautogui.moveTo(1000, 1070)
    click()
    time.sleep(0.5)
    click()

def contains_letter_or_number(s):
    pattern = r'[a-zA-Z0-9]'
    return bool(re.search(pattern, s))

def remove_newlines(string):
    return string.replace("\n", " ")

def image_contains_colour(image, colour):
    image_array = np.array(image)

    hex_color = colour
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

    contains_colour = np.any(np.all(image_array == rgb_color, axis=-1))

    if contains_colour:
        return True
    else:
        return False

# json stuff
def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)  
    except FileNotFoundError:
        return {} 
    except json.JSONDecodeError:
        return {}  

def save_to_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4) 

def add_to_json(file_path, question, options, correct_answer):
    data = load_json_file(file_path)
    options = sorted(options)

    if question not in data:
        data[question] = []

    for i, (option_set, answer) in enumerate(data[question]): 
        if option_set == options:
            data[question][i] = (options, correct_answer)  
            break
    else:
        data[question].append((options, correct_answer))

    save_to_json_file(file_path, data)

def get_answer_from_json(file_path, question, options):
    data = load_json_file(file_path)
    options = sorted(options)

    if question in data:
        for option_set, correct_answer in data[question]:
            if option_set == options:
                return correct_answer  
    return None  

#start answering quesitons
def start_answer():
    answering = True
    question_num = 0
    while answering:
        question_num += 1
        # scroll down
        pyautogui.scroll(-9999)

        # moves mouse out of the way
        pyautogui.moveTo(1850,1070)

        # get screens shots
        print("\ngetting images")
        x1, y1, x2, y2 = 350, 320, 1700, 520
        question_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

        x1, y1, x2, y2 = 425, 515, 925, 690
        a1_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

        x1, y1, x2, y2 = 985, 515, 1485, 690
        a2_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

        x1, y1, x2, y2 = 425, 735, 925, 910 
        a3_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

        x1, y1, x2, y2 = 985, 735, 1485, 910
        a4_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

        # saves screenshots for debugging
        question_screen.save("question.png")
        a1_screen.save("a1.png")
        a2_screen.save("a2.png")
        a3_screen.save("a3.png")
        a4_screen.save("a4.png")

        # converts the screenshots to text
        print("converting images to text")
        question = remove_newlines(pytesseract.image_to_string(question_screen).strip().lower())
        a1 = remove_newlines(pytesseract.image_to_string(a1_screen).strip().lower())
        a2 = remove_newlines(pytesseract.image_to_string(a2_screen).strip().lower())
        a3 = remove_newlines(pytesseract.image_to_string(a3_screen).strip().lower())
        a4 = remove_newlines(pytesseract.image_to_string(a4_screen).strip().lower())

        # detects if it is an image question
        if not contains_letter_or_number(a2) and question_num == 1:
            pyautogui.scroll(9999)
            print("\ndetected image question")
            print("exiting quiz")
            pyautogui.moveTo(800, 1070)
            click()
            top_left()
            click()
            time.sleep(3.5)
            pyautogui.moveTo(50, 35)
            click()
            return

        # print the question
        debug_question = f"{question}: \n1) {a1}, \n2) {a2}, \n3) {a3}, \n4) {a4}"
        print(f"\n{question_num}: {debug_question}")

        print("\ngoing to database")
        
        answer = get_answer_from_json(json_file, question, (a1, a2, a3,a4),)
        top_left()
        if answer:
            print("\nanswer found")
            if answer == a1:
                top_left()
            elif answer == a2:
                top_right()
            elif answer == a3:
                bottom_left()
            elif answer == a4:
                bottom_right()
            else:
                print("\nno answers match, going to ans 1")
            click()

            time.sleep(2)

            x1, y1, x2, y2 = 400, 515, 930, 690
            a1_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

            x1, y1, x2, y2 = 960, 515, 1490, 690
            a2_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

            x1, y1, x2, y2 = 400, 735, 930, 910 
            a3_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

            x1, y1, x2, y2 = 960, 735, 1490, 910
            a4_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

            red = False
            if image_contains_colour(a1_screen, wrong_colour):
                red = True
            elif image_contains_colour(a2_screen, wrong_colour):
                red = True
            elif image_contains_colour(a3_screen, wrong_colour):
                red = True
            elif image_contains_colour(a4_screen, wrong_colour):
                red = True

            if red:
                x1, y1, x2, y2 = 400, 515, 930, 690
                a1_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

                x1, y1, x2, y2 = 960, 515, 1490, 690
                a2_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

                x1, y1, x2, y2 = 400, 735, 930, 910 
                a3_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

                x1, y1, x2, y2 = 960, 735, 1490, 910
                a4_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

                correct_answer = a1
                if image_contains_colour(a1_screen, right_colour):
                    correct_answer = a1
                elif image_contains_colour(a2_screen, right_colour):
                    correct_answer = a2
                elif image_contains_colour(a3_screen, right_colour):
                    correct_answer = a3
                elif image_contains_colour(a4_screen, right_colour):
                    correct_answer = a4

                add_to_json(json_file, question, (a1, a2, a3,a4), correct_answer)
                answer = correct_answer
                print(correct_answer)  
                time.sleep(3)

        else:
            print("\no answer found, adding to data base")
            click()
            time.sleep(1.5)
            x1, y1, x2, y2 = 400, 515, 930, 690
            a1_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

            x1, y1, x2, y2 = 960, 515, 1490, 690
            a2_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

            x1, y1, x2, y2 = 400, 735, 930, 910 
            a3_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

            x1, y1, x2, y2 = 960, 735, 1490, 910
            a4_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

            correct_answer = a1
            if image_contains_colour(a1_screen, right_colour):
                correct_answer = a1
            elif image_contains_colour(a2_screen, right_colour):
                correct_answer = a2
            elif image_contains_colour(a3_screen, right_colour):
                correct_answer = a3
            elif image_contains_colour(a4_screen, right_colour):
                correct_answer = a4

            add_to_json(json_file, question, (a1, a2, a3,a4), correct_answer)
            answer = correct_answer
            print(correct_answer)    

            time.sleep(2)

            x1, y1, x2, y2 = 400, 515, 930, 690
            a1_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

            x1, y1, x2, y2 = 960, 515, 1490, 690
            a2_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

            x1, y1, x2, y2 = 400, 735, 930, 910 
            a3_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

            x1, y1, x2, y2 = 960, 735, 1490, 910
            a4_screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

            red = False
            if image_contains_colour(a1_screen, wrong_colour):
                red = True
            elif image_contains_colour(a2_screen, wrong_colour):
                red = True
            elif image_contains_colour(a3_screen, wrong_colour):
                red = True
            elif image_contains_colour(a4_screen, wrong_colour):
                red = True

            if red:
                time.sleep(3)

        # checks if it is on a question
        print("checking if quiz has ended")
        x1, y1, x2, y2 = 350, 500, 650, 1070
        check_answering = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        check_answering.save("check_answering.png")
        check_text = pytesseract.image_to_string(check_answering).strip().lower()
        if not contains_letter_or_number(check_text):
            print("exiting quiz")
            answering = False
            continue

    # quiz complete
    pyautogui.moveTo(1000,960)
    click()

while True:
    num = random.choice([1,2])
    start_questions(num) 
    start_answer()
    time.sleep(1)

# 175% zoom
# f11 full screen
# may need to change some of the coordingates if screenshots not accurate, detecting wrong text or moving to wrong positions
