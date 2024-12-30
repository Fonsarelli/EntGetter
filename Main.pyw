
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
window.title('Ent Getter')
window.geometry('200x1010')
window.iconbitmap(default='Assets/Images/ent.ico')
window.configure(background='black')
labels = []

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

    # Display ents
    for i in range(len(ents)):
        # Check if label exists
        if (len(labels) > i):
            # Set existing label text
            labels[i][0]['text'] = ents[i][0]
            labels[i][1]['text'] = int((currentTime - ents[i][1]).total_seconds())
        else:
            # New location label
            locationLabel = Label(window, text=ents[i][0])
            locationLabel.grid(column=0, row=i)
            locationLabel.configure(bg='black', fg='white', font=('Arial', 20, 'bold'))

            # New timer label
            timerLabel = Label(window, text=int((currentTime - ents[i][1]).total_seconds()))
            timerLabel.grid(column=1, row=i)
            timerLabel.configure(bg='black', fg='white', font=('Arial', 20, 'bold'))

            # Add label references to list
            labels.append([locationLabel, timerLabel])

    # Clear unused labels
    for i in range(len(ents), len(labels)):
        labels[i][0]['text'] = ""
        labels[i][1]['text'] = ""

    window.after(100, updateWindowInBg)

# Multithreaded update
def updateWindowInBg():
    threading.Thread(target=updateWindow).start()

# Start
updateWindowInBg()
window.mainloop()
