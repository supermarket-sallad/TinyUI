
def onOffToOn(channel: Channel, sampleIndex: int, val: float, 
			  prev: float):

	return

def whileOn(channel: Channel, sampleIndex: int, val: float, 
			prev: float):

	return

def onOnToOff(channel: Channel, sampleIndex: int, val: float, 
			  prev: float):

	return

def whileOff(channel: Channel, sampleIndex: int, val: float, 
			 prev: float):
	return

def onValueChange(channel: Channel, sampleIndex: int, val: float, 
				  prev: float):
	parent().OnMidiEvent(channel.name, val, prev)

	return
