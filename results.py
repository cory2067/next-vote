#!/usr/bin/python
import os
import os.path
import csv
import cgi
import json
import sqlite3
import sys
print "Content-type: text/html\nAccess-Control-Allow-Origin: *\n"
kerb = os.environ['SSL_CLIENT_S_DN_Email'].split('@')[0]

def alert(title, msg): # Show error message and quit
	with open("alert.html", "r") as f:
		data = f.read()

	print data % (title, msg)
	sys.exit(0)

# Load the config file for the election
with open('config.js') as f:
	config = f.read()

config = '\n'.join(config.split('\n')[1:]) #chop var definition
config = json.loads(config)

nexec = ['nenright','mfarejow','cyntlo','cor','bbarajas','jynnie','wpinney','jryang','gfarrell','nmyrie','shavinac']
if not kerb in nexec:
	alert('Error 403', "Only members of Next Exec can view results.")

if not os.path.isfile('results.db'):
	alert("Voting Results", "No results to show.")

conn = sqlite3.connect("results.db")
c = conn.cursor()
votes = c.execute('SELECT * FROM results').fetchall()
conn.close()

print '''<style>
html {
	text-align: center;
	font-family: arial;
}
table {
    margin: 0 auto;
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 50%;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}
</style>'''
print '<table><thead><tr><th>Wing</th>'
for q in config['questions']:
	print '<th>'+q['title']+'</th>'
print '<th>Comment</th></tr></thead>'

freq = ['','<b>Total</b>']
for n,q in enumerate(config['questions']):
	i = n + 2
	a = {}
	for vote in votes: #disgusting
		if vote[i] in a:
			a[vote[i]] += 1
		else:
			a[vote[i]] = 1
	out = ''
	for k,v in sorted(a.items(), key=lambda t: -t[1]):
		out += k + ': ' + str(v) + ',\n'
	freq.append(out)
freq.append('')

for vote in votes+[freq]:
	print '<tr>'
	for q in vote[1:]:
		print '<td>' + q + '</td>'
	print '</tr>'
print '</table>'
