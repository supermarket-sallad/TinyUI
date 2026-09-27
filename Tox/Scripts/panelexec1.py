
from typing import Any
tui = op('TinyUI')
def onOffToOn(panelValue: PanelValue):
	return

def whileOn(panelValue: PanelValue):
	return
def onOnToOff(panelValue: PanelValue):
	return

def whileOff(panelValue: PanelValue):
	return

def onValueChange(panelValue: PanelValue, prev: Any):
	if panelValue.name == "insideu":
		tui.setRolloverU(panelValue.val)
	elif panelValue.name == "insidev":
		tui.setRolloverV(panelValue.val)
	elif panelValue.name == "lselect":
		tui.leftClick(panelValue.val)
	elif panelValue.name == "rselect":
		tui.rightClick(panelValue.val)

	return
