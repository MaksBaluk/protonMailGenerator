# Michi4/Sviatoslav
import pyautogui
import sys
import time
import random
import string
import webbrowser
import ctypes
import re

# Constants
CF_TEXT = 1
kernel32 = ctypes.windll.kernel32
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
user32 = ctypes.windll.user32
user32.GetClipboardData.restype = ctypes.c_void_p


# Function to get 6-digit code from clipboard
def get_clip_6_digit():
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            kernel32.GlobalUnlock(data_locked)
            return str(re.findall(r'(\d{6})', (str(value))))
    finally:
        user32.CloseClipboard()


# Function to get proper email for verification
def get_mail():
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            kernel32.GlobalUnlock(data_locked)
            if "@dropmail.me" in str(value) or "@yomail.info" in str(value):
                match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', str(value))
                res_email = (match.group(0))[1:]
                if "@dropmail.me" in res_email:
                    return res_email
            return False
    finally:
        user32.CloseClipboard()


# Function to generate random information
def randomize(_option_, _length_):
    if _length_ > 0:
        if _option_ == '-p':
            string._characters_ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+'
        elif _option_ == '-s':
            string._characters_ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        elif _option_ == '-l':
            string._characters_ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        elif _option_ == '-n':
            string._characters_ = '1234567890'
        elif _option_ == '-m':
            string._characters_ = 'JFMASOND'

        if _option_ == '-d':
            _generated_info_ = random.randint(1, 28)
        elif _option_ == '-y':
            _generated_info_ = random.randint(1950, 2000)
        else:
            _generated_info_ = ''
            for _counter_ in range(0, _length_):
                _generated_info_ = _generated_info_ + random.choice(string._characters_)

        return _generated_info_

    else:
        return 'error'


# Open ProtonMail signup page
webbrowser.open('https://account.proton.me/signup?plan=free')
time.sleep(10)

# Open new tab in browser
pyautogui.keyDown('ctrlleft')
pyautogui.typewrite('t')
pyautogui.keyUp('ctrlleft')

time.sleep(3)

# Open temporary email service (dropmail.me)
pyautogui.typewrite('https://dropmail.me/\n')

# Scroll down to reveal more emails
pyautogui.keyDown('shift')
pyautogui.keyDown('down')
pyautogui.keyUp('down')
pyautogui.keyUp('shift')
time.sleep(3)

NEW_MAIL = True

# Loop to check for a new email
while True:
    if not NEW_MAIL:
        # Refresh the page
        pyautogui.keyDown('ctrlleft')
        pyautogui.typewrite('r')
        pyautogui.keyUp('ctrlleft')
        time.sleep(5)

    # Select the email address
    pyautogui.keyDown('ctrlleft')
    pyautogui.press('a')
    pyautogui.keyUp('ctrlleft')
    time.sleep(3)

    # Copy the selected email address
    pyautogui.press('select')
    time.sleep(3)
    pyautogui.keyDown('ctrlleft')
    pyautogui.typewrite('c')
    pyautogui.keyUp('ctrlleft')

    # Get the new email
    NEW_MAIL = get_mail()
    if NEW_MAIL:
        print("10 min mail: " + NEW_MAIL)
        break

pyautogui.keyDown('ctrlleft')
pyautogui.typewrite('\t')
pyautogui.keyUp('ctrlleft')
time.sleep(1)

# Generate and type Username
_username_ = randomize('-s', 5) + randomize('-s', 5) + randomize('-s', 5)
pyautogui.typewrite(_username_ + '\t\t\t', interval=0.2)
print("Username:" + _username_)

# Generate and type Password
_password_ = randomize('-p', 16)
pyautogui.typewrite(_password_ + '\t' + _password_ + '\t', interval=0.2)
print("Password:" + _password_)

# Press Enter to submit
pyautogui.typewrite('\n')
time.sleep(5)
# pyautogui.typewrite('\t\t\t\n')
# Type the new email in the ProtonMail signup form


pyautogui.typewrite(NEW_MAIL)
pyautogui.typewrite('\n')

time.sleep(10)

# Copy the email verification code
pyautogui.keyDown('ctrlleft')
pyautogui.typewrite('\t')
pyautogui.keyUp('ctrlleft')
time.sleep(1)

pyautogui.keyDown('ctrlleft')
pyautogui.typewrite('a')
pyautogui.keyUp('ctrlleft')
pyautogui.keyDown('ctrlleft')
pyautogui.typewrite('c')
pyautogui.keyUp('ctrlleft')

# Switch back to the ProtonMail tab
pyautogui.keyDown('ctrlleft')
pyautogui.typewrite('\t')
pyautogui.keyUp('ctrlleft')
time.sleep(5)

# Type the verification code in the ProtonMail form
pyautogui.typewrite(str(get_clip_6_digit()) + '\n')

# Wait for the process to complete
time.sleep(15)

# Finalize the signup
pyautogui.typewrite('\n')
time.sleep(5)
pyautogui.typewrite('\t\t\t\n')
time.sleep(1)
pyautogui.typewrite('\t\n')

# Print the account details
print(_username_ + "@proton.me:" + _password_)

# Save the account details to a log file
logfile = open("accLog.txt", "a")
logfile.write(_username_ + "@proton.me:" + _password_ + "\n")
logfile.close()
