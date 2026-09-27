pComp = parent.TinyUI

def onValueChange(op, fval: float, style: str, label: str, id: int):

	pComp.UpdateParFromTUI(fval, id)

	return
	
def onClick(op, id, internalIndex, leftClick, rightClick):
	pComp.LastClickedID = id
	pComp.LastClickedSubID = internalIndex
	pComp.ArmElement()
	pass

