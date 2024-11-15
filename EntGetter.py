
# Libraries
import requests
import json
from datetime import datetime

class EntGetter:

	def __init__(self, authorisation):
		self.authorisation = authorisation

	# Get events from discord
	def __get_events(self):

		# Define authorisation header
		headers = {
			'authorization': self.authorisation
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

	# Get ent locations
	def get_ents(self, maxAge=120):

		# Get current time
		currentTime = datetime.now()

		# Get events
		events = self.__get_events()

		# Filter events
		ents = []
		for event in events:
			if event[0][:3] == 'ENT':
				ents.append(event)

		# Get ent locations
		locations = []
		for ent in ents:
			location = ent[0].split()[2].replace('*', '')
			time = datetime.strptime(ent[1].split('+')[0], '%Y-%m-%dT%H:%M:%S.%f')
			timeDifference = (currentTime - time).total_seconds()
			if (timeDifference < maxAge):
				locations.append([location, time])

		return locations
