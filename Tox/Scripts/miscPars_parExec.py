
from typing import Any, List

def onValueChange(par: Par, prev: Any):
	if par.name == "Font":
		parent.TinyUI.SetFontFile(par.eval())
	
	elif par.name == "Writeoneffect":
		print(par.eval())
		op("TinyUI").writeOn(par.eval())
	return

def onPulse(par: Par):
	"""
	Called when a parameter is pulsed.
	
	Args:
		par: The Par object that was pulsed
	"""
	return
