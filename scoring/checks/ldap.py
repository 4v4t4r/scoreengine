from __future__ import absolute_import
from config import config
import ldap

# DEFAULTS
ldap_config = {
	'timeout': 5
}
# /DEFAULTS

# CONFIG
if "ldap" in config:
	ldap_config.update(config["ldap"])
# /CONFIG

def check_ldap_lookup(check, data):
	check.addOutput("ScoreEngine: %s Check\n" % (check.getServiceName()))
	check.addOutput("EXPECTED: Sucessful and correct query against the AD (LDAP) server")
	check.addOutput("OUTPUT:\n")

	check.addOutput("Starting check...")

	try:
		# Setup LDAP
		l = ldap.initialize('ldap://%s' % data["HOST"])

		# Bind to the user we're using to lookup
		username = "uid=%s,ou=People,dc=%s,dc=open" % (data["USER"], data["DOMAIN"])
		password = data["PASS"]

		l.protocol_version = ldap.VERSION3
		l.set_option(ldap.OPT_NETWORK_TIMEOUT, ldap_config["timeout"])
		l.simple_bind_s(username, password)

		# We're good!
		check.setPassed()
		check.addOutput("Check successful!")
	except Exception as e:
		check.addOutput("ERROR: %s: %s" % (type(e).__name__, e))

		return