
from typing import Any, Union, List

def onValueChange(cur: Union[Par, List[Par]], prev: Union[Any, List[Any]]):
	parent().UpdateTUIFromPar(cur)
	return

def onExpressionChange(cur: Union[Any, List[Any]], 
					   prev: Union[Any, List[Any]]):
	"""
	Called when parameter expressions change.
	
	Args:
		cur: The current expression(s) (use cur.expr to get current)
		prev: The previous expression(s)
	"""
	# use cur.expr to get current
	return

def onExportChange(cur: Union[Any, List[Any]], 
				   prev: Union[Any, List[Any]]):
	"""
	Called when parameter exports change.
	
	Args:
		cur: The current export(s) (use cur.exportSource to get current)
		prev: The previous export(s)
	"""
	# use cur.exportSource to get current
	return

def onEnableChange(cur: Union[Any, List[Any]], 
				   prev: Union[Any, List[Any]]):
	"""
	Called when parameter enable states change.
	
	Args:
		cur: The current enable state(s) (use cur.enable to get current)
		prev: The previous enable state(s)
	"""
	# use cur.enable to get current
	return

def onModeChange(cur: Union[Any, List[Any]], 
				 prev: Union[Any, List[Any]]):
	"""
	Called when parameter modes change.
	
	Args:
		cur: The current mode(s) (use cur.mode to get current)
		prev: The previous mode(s)
	"""
	# use cur.mode to get current
	return

def onPulse(cur: Union[Any, List[Any]]):
	"""
	Called when parameters are pulsed.
	
	Args:
		cur: The parameter(s) that were pulsed
	"""
	return
