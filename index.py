#!/usr/bin/python
import os
import util
print "Content-type: text/html\nAccess-Control-Allow-Origin: *\n"
kerb = os.environ['SSL_CLIENT_S_DN_Email'].split('@')[0]

if not util.valid_resident(kerb):
	util.alert('Voting Error', "You're not a Next resident!\nIf this is in error, notify next-techchair@mit.edu.")
else:
	util.render('form.html', (util.get_wing(kerb), kerb))
