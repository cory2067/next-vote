#!/usr/bin/python
import os
import os.path
import csv
import cgi
import sqlite3
import sys
import json
print "Content-type: text/html\nAccess-Control-Allow-Origin: *\n"
kerb = os.environ['SSL_CLIENT_S_DN_Email'].split('@')[0]

residents = {} #key is kerberos, value is room
with open("residents.csv", "r") as f:
	res = csv.reader(f)
	for row in res:
		residents[row[1]] = row[0]

def alert(title, msg): # Show error message and quit
	with open("alert.html", "r") as f:
		data = f.read()

	print data % (title, msg)
	sys.exit(0)

form = cgi.FieldStorage()
vote = []
for i,q in enumerate(config['questions']):
	field = 'q' + str(i)
	write = 'write' + str(i)
	if field in form and form['field'] != 'write':
		vote.append(form[field])
	elif write in form and form[write] != '':
		vote.append(form[write])
	else:
		vote.append("Abstain")

if not kerb in residents:
	alert("Voting Error", "You're not a Next resident!")

# Load the config file for the election
with open('config.js') as f:
    config = f.read()

config = '\n'.join(config.split('\n')[1:]) #chop var definition
config = json.loads(config)

def get_wing(kerb):
	room = residents[kerb]
	floor = room[0]
	side = 'E' if int(room[1:])>30 else 'W'
	return floor+side

init = not os.path.isfile("results.db")
conn = sqlite3.connect("results.db")
c = conn.cursor()

nstr = ''
qstr = ''
for i,q in enumerate(config['questions']):
	nstr += q + int(i) + ' text, '
	qstr += '?,'
nstr = nstr[:-2]
qstr = qstr[:-1]
print(nstr)
print(qstr)

sys.exit(0)
if init:
	c.execute("CREATE TABLE results (name text, wing text, vote text)")
	conn.commit()

voted = c.execute('SELECT * FROM results WHERE name=?', (kerb,)).fetchall()
if len(voted):
	alert("Voting Error", "You've already voted.")

c.execute('INSERT INTO results VALUES (?,?,?)', (kerb, get_wing(kerb), vote))
conn.commit()
conn.close()

alert("Success", "Your vote has been recorded.")
