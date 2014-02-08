from slope import *
from tangent import *

def get_notes(notekey):
	if 'slope' in notekey:
		return slope(notekey)
	elif 'tangent' in notekey:
		return tangent(notekey)
	elif 'under_construction' in notekey:
		return 'The rest of this unit is under construction; please check back at a later time!'