#!/usr/bin/python
import os
import os.path
import cgi
import sqlite3
import util

print "Content-type: text/html\nAccess-Control-Allow-Origin: *\n"
kerb = os.environ['SSL_CLIENT_S_DN_Email'].split('@')[0]

# Load the config file for the election
config = util.load_config()

form = cgi.FieldStorage()
vote = []
for i,q in enumerate(config['questions']):
	field = 'q' + str(i)
	write = 'write' + str(i)
	if field in form and form[field].value != 'write':
		vote.append(form[field].value) # handle normal votes
	elif write in form and form[write].value != '':
		vote.append(form[write].value) # handle write in
	else:
		vote.append("Abstain") # if no valid input specified

comment = ''
if 'comment' in form:
	comment = form['comment'].value

if not util.valid_resident(kerb):
	util.alert("Voting Error", "You're not a Next resident!")

init = not os.path.isfile("results.db")
conn = sqlite3.connect("results.db")
c = conn.cursor()

nstr = ''
qstr = ''
for i,q in enumerate(config['questions']):
	nstr += 'q' + str(i) + ' text, ' # build up query string for creating table
	qstr += '?,' # build up a query string for inserting into the database
nstr = nstr[:-2]
qstr = qstr[:-1]


if init: #if the database doesn't exist yet
	c.execute("CREATE TABLE results (name text, wing text, "+nstr+",comment text)")
	conn.commit()

voted = c.execute('SELECT * FROM results WHERE name=?', (kerb,)).fetchall()
if len(voted):
	util.alert("Voting Error", "You've already voted.")

t = tuple([kerb, get_wing(kerb)] + vote + [comment]) # compile together name, votes, comment
c.execute('INSERT INTO results VALUES (?,?,?,'+qstr+')', t)
conn.commit()
conn.close()

util.alert("Success", "Your vote has been recorded.")
