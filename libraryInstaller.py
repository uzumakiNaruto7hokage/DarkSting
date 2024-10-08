import subprocess

libraries = ["pyautogui","pyperclip","pygame","requests"]

for i in libraries:
    print("installing",i)
    code = "pip install "+i
    try:
        subprocess.run(code, shell=True, capture_output=True, text=True)
        print(i,"installed succesfully")
    except:
        print("installation failed for",i)