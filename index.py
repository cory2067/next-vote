#!/usr/bin/python
import os
import csv
print "Content-type: text/html\nAccess-Control-Allow-Origin: *\n"
kerb = os.environ['SSL_CLIENT_S_DN_Email'].split('@')[0]

residents = {} #key is kerberos, value is room
with open("residents.csv", "r") as f:
	res = csv.reader(f)
	for row in res:
		residents[row[1]] = row[0]

def get_wing(kerb):
	room = residents[kerb]
	floor = room[0]
	side = 'E' if int(room[1:])>30 else 'W'
	return floor+side

if not kerb in residents:
	with open("alert.html", "r") as f:
		data = f.read()

	print data % ("Voting Error", "You're not a Next resident!\nIf this is in error, notify next-techchair@mit.edu.")
else:
	with open("form.html", "r") as f:
		data = f.read()

	print data % (kerb, get_wing(kerb))
