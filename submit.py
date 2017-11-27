#!/usr/bin/python
import os
import os.path
import csv
import cgi
import sqlite3
import sys
print "Content-type: text/html\nAccess-Control-Allow-Origin: *\n"
kerb = os.environ['SSL_CLIENT_S_DN_Email'].split('@')[0]

residents = {} #key is kerberos, value is room
with open("residents.csv", "r") as f:
	res = csv.reader(f)
	for row in res:
		residents[row[1]] = row[0]

form = cgi.FieldStorage()
if not 'choice' in form:
	print "Invalid vote. Are you sure you chose a candidate?"
	sys.exit(0)

vote = form['choice'].value
if 'write' in vote:
	if 'write' in form:
		vote = form['write'].value
	else:
		print "Invalid vote. You didn't type a write-in candidate."

if not kerb in residents:
	print "Error: You're not a Next resident! <br/>"
	print "If you believe you received this in error, please notify next-techchair@mit.edu"
	sys.exit(0)

def get_wing(kerb):
	room = residents[kerb]
	floor = room[0]
	side = 'E' if int(room[1:])>30 else 'W'
	return floor+side

init = not os.path.isfile("results.db")
conn = sqlite3.connect("results.db")
c = conn.cursor()
if init:
	c.execute("CREATE TABLE results (name text, wing text, vote text)")
	conn.commit()

voted = c.execute('SELECT * FROM results WHERE name=?', (kerb,)).fetchall()
if len(voted):
	print "You've already voted."
	sys.exit(0)

c.execute('INSERT INTO results VALUES (?,?,?)', (kerb, get_wing(kerb), vote))
conn.commit()
conn.close()

print 'Your vote has been recorded!'
print '<script>window.location = "https://next.scripts.mit.edu/vote/budget"</script>'
