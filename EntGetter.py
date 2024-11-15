
# Sources
# https://www.youtube.com/watch?v=xh28F6f-Cds

# Imports
import requests
import json
import os
from datetime import datetime
import time
import pygame

# Define clear console
clear = lambda: os.system('cls')

# Initialise pygame
pygame.init()
notification = pygame.mixer.Sound('ent-notification.wav')

# Retrieve events from discord
def retrieve_events(authorisation):

	# Define authorisation header
	headers = {
		'authorization': authorisation
	}

	# Request messages from channel
	r = requests.get('https://discord.com/api/v9/channels/1166753438177173534/messages', headers=headers)

	# Get events from JSON
	events = []
	messages = json.loads(r.text)
	for value in messages:
		events.append([value['content'], value['timestamp']])
	events.reverse()

	return events

# Print ent locations
def print_ents(authorisation, old):

	# Get current time
	currentTime = datetime.now()

	# Get events
	events = retrieve_events(authorisation)

	# Filter events
	ents = []
	for event in events:
		if event[0][:3] == 'ENT':
			ents.append(event)

	# Print ent locations
	clear()
	print()
	new = []
	for ent in ents:
		location = ent[0].split()[2].replace('*', '')
		time = datetime.strptime(ent[1].split('+')[0], '%Y-%m-%dT%H:%M:%S.%f')
		timeDifference = (currentTime - time).total_seconds()
		if (timeDifference < 120):
			print('   ' + location, int(timeDifference))
			new.append(ent)
	print()

	# Play notification sound
	if (new != old):
		if (len(new) > len(old)):
			notification.play()

	return new

# Main
def main():

	# Get authorisation as input
	clear()
	authorisation = input("Authorisation: ")
	notification.play()

	# Main loop
	old = []
	while True:
		time.sleep(0.5)
		old = print_ents(authorisation, old)

main()
