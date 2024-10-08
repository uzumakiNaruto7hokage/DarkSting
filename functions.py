import subprocess
import pyperclip
import pyautogui
import webbrowser
import tkinter as tk
from tkinter import messagebox
import requests
import pygame
from time import sleep

root = tk.Tk()
root.withdraw()

def play_mp3(file_path):
    sleep(1)
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def shutDown():
    code = "shutdown /s /t 0"
    try:
        subprocess.run(code, shell=True, capture_output=True, text=True)
        
    except:
        pass
    
def restart():
    code = "restart /r /f /t 0"
    try:
        subprocess.run(code, shell=True, capture_output=True, text=True)
        
    except:
        pass
    
def disableClipboard(str):
    pyperclip.copy(str)

def disableMouse(x,y):
    pyautogui.moveTo(x,y)
    
def openUrl(url):
    webbrowser.open(url)

def typeText(text):
    pyautogui.typewrite(text)

def closeWindow():
    pyautogui.hotkey("fn","alt","f4","enter")

def download_file(url, name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    
def makeMsgBox(type,title,text):
    print("making a msg box")
    if type == "warning":
        messagebox.showwarning(title,text)
    if type == "info":
        messagebox.showinfo(title,text)
    if type == "warning":
        messagebox.showwarning(title,text)
    if type == "error":
        messagebox.showerror(title,text)
    if type == "question":
        messagebox.askquestion(title,text)
        
