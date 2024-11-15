
# Libraries
from EntGetter import EntGetter
from datetime import datetime
import pygame
from tkinter import *
import threading

# Initialise EntGetter
entGetter = EntGetter('') # INSERT DISCORD AUTHORISATION HERE
previousEnts = []

# Initialise pygame sound
pygame.init()
notification = pygame.mixer.Sound('Assets/Sounds/ent-notification.wav')

# Set window properties
window = Tk()
window.title('Ent')
window.geometry('200x1010')
window.iconbitmap(default='Assets/Images/ent.ico')
window.configure(background='black')

# Update loop
def updateWindow():

    # Get current time
    currentTime = datetime.now()
     
    # Get ents
    ents = entGetter.get_ents()

    # Check for notiication
    global previousEnts
    if (ents != previousEnts):
        if(len(ents) > len(previousEnts)):
            notification.play()
    previousEnts = ents

    # Clear window
    for widget in window.winfo_children():
        widget.destroy()

    # Display ents
    for i in range(len(ents)):
        # Location label
        locationLabel = Label(window, text=ents[i][0])
        locationLabel.grid(column=0, row=i)
        locationLabel.configure(bg='black', fg='white', font=('Arial', 25, 'bold'))

        # Timer label
        timer = int((currentTime - ents[i][1]).total_seconds())
        timerLabel = Label(window, text=timer)
        timerLabel.grid(column=1, row=i)
        timerLabel.configure(bg='black', fg='white', font=('Arial', 25, 'bold'))

    window.after(100, updateWindowInBg)

# Multithreaded update
def updateWindowInBg():
    threading.Thread(target=updateWindow).start()

# Start
updateWindowInBg()
window.mainloop()
