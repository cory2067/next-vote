#!/usr/bin/python
import os
import os.path
import cgi
import sqlite3
import util
print "Content-type: text/html\nAccess-Control-Allow-Origin: *\n"
kerb = os.environ['SSL_CLIENT_S_DN_Email'].split('@')[0]

config = util.load_config()

nexec = ['nenright','mfarejow','cyntlo','cor','bbarajas','jynnie','wpinney','jryang','gfarrell','nmyrie','shavinac']
if not kerb in nexec:
	util.alert('Error 403', "Only members of Next Exec can view results.")

if not os.path.isfile('results.db'):
	util.alert("Voting Results", "No results to show.")

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
# Iterate through all question IDs
for i in range(2, 2+len(config['questions'])):
	a = {}
	for vote in votes:
		if vote[i] in a:
			a[vote[i]] += 1 #tally up votes
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
