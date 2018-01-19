import sys
import csv
import json

residents = {} #key is kerberos, value is room
with open("residents.csv", "r") as f:
	res = csv.reader(f)
	for row in res:
		residents[row[1]] = row[0]

# render an HTML template
def render(template, params):
	with open(template, "r") as f:
		data = f.read()

	print data % params

def alert(title, msg): # Show error message and quit
	print render('alert.html', (title, msg))
	sys.exit(0)

'''
def get_residents():
	residents = {} #key is kerberos, value is room
	with open("residents.csv", "r") as f:
		res = csv.reader(f)
		for row in res:
			residents[row[1]] = row[0]
'''

def load_config():
	with open('config.js') as f:
	    config = f.read()

	config = '\n'.join(config.split('\n')[1:]) #chop var definition
	return json.loads(config)

def get_wing(kerb):
	room = residents[kerb]
	floor = room[0]
	side = 'E' if int(room[1:])>30 else 'W'
	return floor+side

def valid_resident(kerb):
	return kerb in residents
