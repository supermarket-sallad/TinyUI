
from TDStoreTools import StorageManager
import TDFunctions as TDF
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict

class ElementType(Enum):
	emptyLine 		= 0
	divider 		= 1
	slider 			= 2
	button 			= 3
	menu 			= 4
	stepper 		= 5
	bitPattern 		= 6
	stringDisplay 	= 7
	littleAnimation = 8

@dataclass
class UIElement:
	id: 			int
	type:  			ElementType
	label:			str
	parName:		str
	interactive:	bool
	rangeMin:		float
	rangeMax:       float
	numElements:	int
	menuOptions:    list[str]
	toggleMode:		bool = False
	siblingParName: str  = ""

@dataclass
class MidiElement:
	par: td.Par = None
	subElement: int  = -1
	
class TinyUIExt:
	"""
	TinyUIExt description
	"""
	def __init__(self, ownerComp):
		self.ownerComp   	 = ownerComp
		self.elements    	 = []
		self.parToElement 	 = defaultdict(UIElement)
		
		self.tui         	       = self.ownerComp.op('TinyUI')
		self.fromPar 	 	 	   = False
		self.LastClickedID   	   = None
		self.LastClickedSubID	   = None

		##-----midi mapping---##
		self.midiChanToPar 				= defaultdict(list)
		self.armedElement: UIElement    = None
		self.MAX_MIDI_VAL = 127.0
		self.MIDI_CHAN_PICKUP = True
	

		storedItems = [
			{'name': 'PickledLayout',   'default': None, 'readOnly': False,'property': True, 'dependable': True},
			{'name': 'PickledMidiMaps', 'default': None, 'readOnly': False,'property': True, 'dependable': True}
			]

		self.stored = StorageManager(self, ownerComp, storedItems)

##-----------layout building
	def Clear(self) -> None:
		self.midiChanToPar   = defaultdict(list)
		self.PickledLayout   = []
		self.PickledMidiMaps = []
		self._clearPars()
		self.elements        = []
		self.tui.clearLayout()
		self.ownerComp.par.Animationframe.expr = ""


	def Remove(self, id: int = -1) -> None:
		if id == -1: id = self.LastClickedID
		if not (0 <= id < len(self.elements)): return
		element = self.elements[id]
		self._destroyElementPars(element)
		del self.elements[id]
		self._reindexElements()
		run(lambda: self._finishRemove(), delayFrames=1)

	def Insert(self, id: int, function): ##idk how to call this
		#insert an element after the id
		#rebuild self.tui
		pass
	
	def AddSlider(self, label: str = "", rangeMin: float = 0, rangeMax: float = 1, interactive: bool = True) -> UIElement:
		element = UIElement(id = self._assignID(),
							type 		= ElementType.slider,
							label 		= label or "val",
							parName 	= self._getUniqueParName(label),
							interactive = interactive,
							rangeMin 	= rangeMin,
							rangeMax 	= rangeMax,
							numElements = 1,
							menuOptions = [],
							)
		self.elements.append(element)
		self._createPar(element)
		self._addToTUI(element)
		self._appendToPickeledLayout(element)
		return element
	
	def AddDivider(self, label: str = "") -> UIElement:
		element = UIElement(id          = self._assignID(),
							type        = ElementType.divider,
							label       = label,
							parName     = None,
							interactive = False,
							rangeMin 	= 0,
							rangeMax 	= 1,
							numElements = 1,
							menuOptions = [],)
		
		self.elements.append(element)
		self._addToTUI(element)
		self._appendToPickeledLayout(element)

		return element
	
	def AddEmptyLine(self) -> UIElement:
		element = UIElement(id = self._assignID(),
							type = ElementType.emptyLine,
							parName = None,
							label = None,
							interactive = False,
							rangeMin = None,
							rangeMax = None,
							numElements = 1,
							menuOptions = None)	
		
		self._addToTUI(element)
		self.elements.append(element)
		self._appendToPickeledLayout(element)
		return element

	def AddMenu(self, label: str = "", menuOptions: list[str] = ["option1", "option2", "option3"]) -> UIElement:
		element = UIElement(id = self._assignID(),
							type = ElementType.menu,
							label = label or "menu",
							parName = self._getUniqueParName(label),
							interactive=True,
							rangeMin = 0,
							rangeMax = 1,
							numElements = 1,
							menuOptions = menuOptions,
		)
		self.elements.append(element)
		self._createPar(element)
		self._addToTUI(element)
		self._appendToPickeledLayout(element)
		return element
	
	def AddButtons(self, label: str = "", toggleMode = True, numButtons: int = 1, interactive = True) -> UIElement:
		numButtons = tdu.clamp(numButtons, 1, 4)
		element = UIElement(id          = self._assignID(),
							type        = ElementType.button,
							label       = label or "btns",
							parName     = self._getUniqueParName(label),
							interactive = interactive,
							rangeMin    = 0,
							rangeMax    = 1,
							numElements = numButtons,
							menuOptions = [],
							toggleMode=toggleMode,
							)
		self.elements.append(element)
		self._createPar(element)
		self._addToTUI(element)
		self._appendToPickeledLayout(element)

		return element

	def AddStepper(self, label: str = "", rangeMin: int = -10, rangeMax: int = 10) -> UIElement:
		element = UIElement(id = self._assignID(),
							type = ElementType.stepper,
							label = label or "int",
							parName = self._getUniqueParName(label),
							interactive = True,
							rangeMin = rangeMin,
							rangeMax = rangeMax,
							numElements = 1,
							menuOptions = [],
							toggleMode = False,
							)
		self.elements.append(element)
		self._createPar(element)
		self._addToTUI(element)
		self._appendToPickeledLayout(element)
		return element
	
	def AddLittleAnimation(self) -> UIElement:
		element = UIElement(id = self._assignID(),
							type = ElementType.littleAnimation,
							label = "0_o",
							parName = None,
							rangeMin = 0,
							rangeMax = 1,
							interactive = False,
							numElements = 1,
							menuOptions = [],
							toggleMode = False
							)
		self.elements.append(element)
		self._addToTUI(element)
		self._appendToPickeledLayout(element)
		self.ownerComp.par.Animationframe.expr = "absTime.frame % 64 / 8"
		return element
	
	def AddBitPattern(self, numSteps: int = 8) -> UIElement:
		element = UIElement(id = self._assignID(),
							type=ElementType.bitPattern,
							label = "Sequencer1",
							parName = self._getUniqueParName("Sequencer1"),
							rangeMin = 0,
							rangeMax = 1,
							numElements = numSteps,
							menuOptions=[],
							toggleMode=False,
							interactive = True,
							)
		self._addToTUI(element)
		self._createPar(element)
		self.elements.append(element)
		self._appendToPickeledLayout(element)

		return element

##-------tui
	def _addToTUI(self, element: UIElement) -> None:
		match(element.type):
			case(ElementType.slider):
				self.tui.addSlider(element.label, element.rangeMin, element.rangeMax, element.interactive)
				return
			case(ElementType.emptyLine):
				self.tui.addEmptyLine()
				return
			case(ElementType.divider):
				self.tui.addDivider(element.label)
				return
			case(ElementType.menu):
				self.tui.addMenu(element.label, list(element.menuOptions), False)
				return
			case(ElementType.button):
				self.tui.addButton(element.label, element.toggleMode, element.interactive, element.numElements)
				return
			case(ElementType.stepper):
				self.tui.addStepper(element.label, element.rangeMin, element.rangeMax)
				return
			case(ElementType.littleAnimation):
				self.tui.addLittleAnimation()
				return
			case(ElementType.bitPattern):
				self.tui.addBitPattern(element.numElements)
				return
	
	def _rebuildTUI(self) -> None:
		self.tui.clearLayout()
		for element in self.elements:
			self._addToTUI(element)
			
##---------parameters
	def _clearPars(self):
		for parGroup in self.ownerComp.customPages["PARAMS"].parGroups:
			parGroup.destroy()
	
	def _createPar(self, element: UIElement) -> None:
		match(element.type):
			case(ElementType.slider):
				par = self._createSliderPar(element)
				self.parToElement[par] = element
			case(ElementType.menu):
				par = self._createMenuPar(element)
				self.parToElement[par] = element
			case(ElementType.button):
				par = self._createButtonPar(element)
				self.parToElement[par] = element
			case(ElementType.stepper):
				par = self._createStepperPar(element)
				self.parToElement[par] = element
			case(ElementType.bitPattern):
				par = self._createBitPatternPar(element)
				self.parToElement[par] = element

	def _createSliderPar(self, element: UIElement) -> td.Par:
		page = self.ownerComp.customPages["PARAMS"]
		par = page.appendFloat(element.parName)
		par.normMin = element.rangeMin
		par.normMax = element.rangeMax
		par.label   = element.label
		return par
	
	def _createMenuPar(self, element: UIElement) -> td.Par:
		page = self.ownerComp.customPages["PARAMS"]
		par = page.appendMenu(element.parName)
		par[0].menuNames  = element.menuOptions
		par[0].menuLabels  = element.menuOptions
		par.label = element.label
		return par

	def _createButtonPar(self, element: UIElement) -> td.Par:
		page = self.ownerComp.customPages["PARAMS"]
		par = page.appendToggle(element.parName, size = element.numElements) if element.toggleMode else page.appendMomentary(element.parName, size = element.numElements)
		par.label = element.label
		return par

	def _createStepperPar(self, element: UIElement) -> td.Par:
		page = self.ownerComp.customPages["PARAMS"]
		par = page.appendInt(element.parName)
		par.normMin = element.rangeMin
		par.normMax = element.rangeMax
		par.label = element.label
		return par
	
	def _createBitPatternPar(self, element: UIElement) -> td.Par:
		page = self.ownerComp.customPages["PARAMS"]
		patternPar = page.appendInt(element.parName)
		patternPar.normMax = 2**element.numElements - 1
		patternPar.normMin = 0
		patternPar.val = 2**element.numElements - 1
		patternPar.min = 0
		patternPar.max = 2**element.numElements - 1

		curStepPar = page.appendInt(patternPar.name + "step")
		element.siblingParName = curStepPar.name
		curStepPar.label = patternPar.name + " Current Step"
		curStepPar.normMax = element.numElements
		curStepPar.normMin = 0
		return patternPar
		
	def _destroyElementPars(self, element: UIElement) -> td.Par:
		if not element.parName: return
		parGroup = self.ownerComp.parGroup[element.parName]
		if parGroup is None: return
		for par in list(self.parToElement.keys()):
			if(self.parToElement[par] is element):
				del self.parToElement[par]
		parGroup.destroy()

		if element.siblingParName:
			siblingGroup = self.ownerComp.parGroup[element.siblingParName]
			if siblingGroup is not None:
				siblingGroup.destroy()

		
##--------updating
	##------------from par
	def UpdateTUIFromPar(self, par: td.ParGroup):
		self.fromPar = True
		element = self.parToElement.get(par)
		
		if self._isStepParameter(par):
			self._updateBitPatternSequenceStep(par)

		if element is None: return

		match(element.type):
			case(ElementType.slider):
				self._updateSliderFromPar(element, par)
			case(ElementType.menu):
				self._updateMenuFromPar(element, par)
			case(ElementType.button):
				self._updateButtonFromPar(element, par)
			case(ElementType.stepper):
				self._updateStepperFromPar(element, par)
			case(ElementType.bitPattern):
				self._updateBitPatternFromPar(element, par)
				
	def _updateSliderFromPar(self, element: UIElement, par: td.ParGroup) -> None:
		self.tui.setValue(element.id, par[0].val)

	def _updateMenuFromPar(self, element: UIElement, par: td.ParGroup) -> None:
		self.tui.setValue(element.id, par[0].menuIndex)

	def _updateButtonFromPar(self, element: UIElement, par: td.ParGroup) -> None:
		ival = self._tupleBitsToInt(par.eval())
		self.tui.setValue(element.id, ival)

	def _updateStepperFromPar(self, element: UIElement, par: td.ParGroup) -> None:
		self.tui.setValue(element.id, par[0].val)

	def _updateBitPatternFromPar(self, element: UIElement, par: td.ParGroup) -> None:
		self.tui.setValue(element.id, par, self.ownerComp.par[element.siblingParName])

	def _updateBitPatternSequenceStep(self, par: td.ParGroup) -> None:
		patternPar = self.ownerComp.parGroup[par.name.removesuffix("step")]
		print(patternPar)
		element = self.parToElement.get(patternPar)
		self.tui.setValue(element.id, patternPar[0].eval(), par[0].eval())
		pass
	
	##-----------from TUI
	def UpdateParFromTUI(self, fval: float, id: int) -> None:
		if self.fromPar: 
			self.fromPar = False
			#return
		element = self.elements[id]
		par = self.ownerComp.parGroup[element.parName]
		if par is None: return None
		match(element.type):
			case(ElementType.slider):
				self._updateSliderFromTUI(par, fval)
			case(ElementType.menu):
				self._updateMenuFromTUI(par, fval)
			case(ElementType.stepper):
				self._updateStepperFromTUI(par, fval)
			case(ElementType.button):
				self._updateButtonsFromTUI(par, fval)
			case(ElementType.bitPattern):
				self._updateBitPatternFromTUI(par, fval)

	def _updateSliderFromTUI(self, par: td.ParGroup, fval: float) -> None:
		par.val = fval

	def _updateMenuFromTUI(self, par: td.ParGroup, fval: float) -> None:
		par.menuIndex = int(fval)

	def _updateStepperFromTUI(self, par: td.ParGroup, fval: float) -> None:
		par.val = int(fval)

	def _updateButtonsFromTUI(self, par, fval):
		ival = int(fval)
		for i in range(len(par)):
			par[i].val = self._isBitActive(ival, i)

	def _updateBitPatternFromTUI(self, par, fval):
		par.val = int(fval)

##---------helpers
	def _getLegalParName(self, label: str) -> str:
		name = label.strip().lower()
		name = re.sub(r'[^A-Za-z0-9]+', '', name)
		if not name:
			return 'Par'
		if name[0].isdigit():
			return 'Par' + name
		name = name[0].upper() + name[1:]
		return name
	
	def _getUniqueParName(self, label: str) -> str:
		base = self._getLegalParName(label)

		# Names currently known to TouchDesigner
		existingNames = {
			par.name
			for par in self.ownerComp.customPars
		}

		# Names already reserved by this UI, including parameters
		# that may not have been created yet.
		reservedNames = {
			e.parName
			for e in self.elements
			if e.parName
		}

		usedNames = existingNames | reservedNames

		if base not in usedNames:
			return base

		i = 1
		while f"{base}{i}" in usedNames:
			i += 1

		return f"{base}{i}"

	def _assignID(self) -> int:
		return len(self.elements)

	def _isBitActive(self, val: int, index: int) -> bool:
		return (val & (1 << index)) != 0

	def _tupleBitsToInt(self, bits: tuple[bool, ...]) -> int:
		return sum(bit << i for i, bit in enumerate(bits))

	def _toggleBit(self, ival: int, bitIndex: int) -> int:
		return ival ^ (1 << bitIndex)

	def _isStepParameter(self, par):
		return re.fullmatch(r"Sequencer\d+step", par[0].name) is not None

	def GetElement(self, id: int):
		return self.elements[id]
	
##-----rebuilding
	def _elementToDict(self, element: UIElement) -> dict:
		return {
			'id':             element.id,
			'type':           element.type.value,
			'label':          element.label,
			'parName':        element.parName,
			'interactive':    element.interactive,
			'rangeMin':       element.rangeMin,
			'rangeMax':       element.rangeMax,
			'numElements':    element.numElements,
			'menuOptions':    list(element.menuOptions) if element.menuOptions else [],
			'toggleMode':     element.toggleMode,
			'siblingParName': element.siblingParName,
		}

	def _dictToElement(self, d: dict) -> UIElement:
		d = dict(d)
		d['type'] = ElementType(d['type'])
		return UIElement(**d)

	def _saveFullLayout(self):
		self.PickledLayout = [self._elementToDict(e) for e in self.elements]

	def _appendToPickeledLayout(self, element: UIElement):
		self.PickledLayout.append(self._elementToDict(element))

	def _rebuildLayout(self):
		data = self.PickledLayout
		if not data:
			return

		data = sorted(data, key=lambda d: d['id'])

		self.tui.clearLayout()
		self.elements = []
		self.parToElement = {}

		for d in data:
			element = self._dictToElement(d)
			self.elements.append(element)

			if element.parName:
				par = self.ownerComp.parGroup[element.parName]
				if par is not None:
					self.parToElement[par] = element

			self._addToTUI(element)

	def _reindexElements(self):
		for i, element in enumerate(self.elements):
			element.id = i

	def _finishRemove(self):
		self._saveFullLayout()
		self._rebuildTUI()
##----------------MIDI MAPPING
	def OnMidiEvent(self, chanName: str, chanVal: float, prevChanVal):
		chanVal /= self.MAX_MIDI_VAL
		prevChanVal /= self.MAX_MIDI_VAL
		self._driveMidi(chanName, chanVal, prevChanVal)
		
		if not self.ownerComp.par.Midimap.eval(): return
		if self.armedElement is None: return
		self._mapMidi(chanName)
		self.armedElement = None
		return

	def ArmElement(self):
		if self.LastClickedID < 0: return
		self.armedElement = self.elements[self.LastClickedID]

	def RemoveAllMidiMapping(self):
		self.PickledMidiMaps = []
		self.midiChanToPar = defaultdict(list)
		return
		
	def _mapMidi(self, chanName: str):
		element  = self.armedElement
		parGroup = self.ownerComp.parGroup[element.parName]
		if parGroup is None: return

		subElement = max(self.LastClickedSubID or 0, 0)
		par = parGroup[subElement]

		midiElement = MidiElement(par, subElement)
		self.midiChanToPar[chanName].append(midiElement)
		self._appendToMIDIStorage(chanName, midiElement)	
		self.armedElement = None
		return
		
	def _driveMidi(self, chanName, chanVal, prevChanVal):
		midiElements = self.midiChanToPar.get(chanName)
		if midiElements is None: return

		for midiElement in midiElements:
			parGroup = midiElement.par.parGroup
			element = self.parToElement.get(parGroup)
			if element is None: continue

			match(element.type):
				case(ElementType.button):
					self._driveButtons(midiElement, chanVal, prevChanVal, element.toggleMode)
					continue
				case(ElementType.slider):
					self._driveSlider(midiElement, chanVal, prevChanVal)
					continue
				case(ElementType.stepper):
					self._driveStepper(midiElement, chanVal, prevChanVal)
					continue
				case(ElementType.menu):
					self._driveMenu(midiElement, chanVal, prevChanVal)
				case(ElementType.bitPattern):
					self._driveBitPattern(midiElement, chanVal, prevChanVal)
		return

	def _driveButtons(self, midiElement, chanVal, prevChanVal, toggle):
		if toggle:
			if chanVal > 0.5 and prevChanVal < 0.5:
				midiElement.par.val = not(midiElement.par.eval())
		else:
			midiElement.par.val = chanVal > 0.5
		pass

	def _driveSlider(self, midiElement, chanVal, prevChanVal):
		if not self.MIDI_CHAN_PICKUP:
			midiElement.par.val = tdu.remap(chanVal, 0.0, 1.0, midiElement.par.normMin, midiElement.par.normMax)
			return

		rvalCur = tdu.remap(chanVal, 0.0, 1.0, midiElement.par.normMin, midiElement.par.normMax)
		rvalPrev = tdu.remap(prevChanVal, 0.0, 1.0, midiElement.par.normMin, midiElement.par.normMax)
		parVal = midiElement.par.eval()

		if abs(rvalPrev - parVal) < 0.02:
			midiElement.par.val = rvalCur
			return

		lo, hi = min(rvalCur, rvalPrev), max(rvalCur, rvalPrev)
		if lo <= parVal <= hi:
			midiElement.par.val = rvalCur
			return
		return

	def _driveStepper(self, midiElement, chanVal, prevChanVal):
		if not self.MIDI_CHAN_PICKUP:
			midiElement.par.val = tdu.remap(chanVal, 0.0, 1.0, midiElement.par.normMin, midiElement.par.normMax)
			return

		rvalCur = tdu.remap(chanVal, 0.0, 1.0, midiElement.par.normMin, midiElement.par.normMax)
		rvalPrev = tdu.remap(prevChanVal, 0.0, 1.0, midiElement.par.normMin, midiElement.par.normMax)
		parVal = midiElement.par.eval()

		if abs(rvalPrev - parVal) < 1:
			midiElement.par.val = rvalCur
			return

		lo, hi = min(rvalCur, rvalPrev), max(rvalCur, rvalPrev)
		if lo <= parVal <= hi:
			midiElement.par.val = rvalCur
			return
		return
	
	def _driveMenu(self, midiElement, chanVal, prevChanVal):
		if chanVal > 0.5 and prevChanVal < 0.5:
			midiElement.par.menuIndex = midiElement.subElement
		return

	def _driveBitPattern(self, midiElement, chanVal, prevChanVal):
		if chanVal > 0.5 and prevChanVal < 0.5:
			midiElement.par.val = self._toggleBit(midiElement.par.eval() , midiElement.subElement)
		return

	def _appendToMIDIStorage(self, chanName: str, midiElement: MidiElement):
		current = list(self.PickledMidiMaps) if self.PickledMidiMaps else []
		current.append(self._midiElementToDict(chanName, midiElement))
		self.PickledMidiMaps = current

	def _rebuildMidiLookupsFromLayout(self):
		self.midiChanToPar = defaultdict(list)
		data = self.PickledMidiMaps
		if not data:
			return

		for d in data:
			parGroup = self.ownerComp.parGroup[d['parName']]
			if parGroup is None:
				continue

			element    = self.parToElement.get(parGroup)
			subElement = d['subElement']

			if element is not None and not self._parGroupIsIndexedBySubElement(element.type):
				par = parGroup[0]
			else:
				if subElement >= len(parGroup):
					continue
				par = parGroup[subElement]

			self.midiChanToPar[d['chanName']].append(MidiElement(par, subElement))

	def _midiElementToDict(self, chanName: str, midiElement: MidiElement) -> dict:
		return {
			'chanName':   chanName,
			'parName':    midiElement.par.parGroup.name,
			'subElement': midiElement.subElement,
		}

	def _parGroupIsIndexedBySubElement(self, elementType: ElementType) -> bool:
		return elementType not in (ElementType.menu, ElementType.bitPattern)


##------misc
	def SetFontFile(self, name):
		if name == "JetBrainsMono":
			self.ownerComp.par.fontfile.expr = "f'vfs:{me}:JetBrainsMono[wght].ttf'"
			self.ownerComp.par.Fontaspect = 0.6
		elif name == "ShareTechMono":
			self.ownerComp.par.fontfile.expr = "f'vfs:{me}:ShareTechMono-Regular.ttf'"
			self.ownerComp.par.Fontaspect = 0.53
		elif name == "Lekton-Bold":
			self.ownerComp.par.fontfile.expr = "f'vfs:{me}:Lekton-Bold.ttf'"
			self.ownerComp.par.Fontaspect = 0.5
		elif name == "Lekton-Regular":
			self.ownerComp.par.fontfile.expr = "f'vfs:{me}:Lekton-Regular.ttf'"
			self.ownerComp.par.Fontaspect = 0.5
			
##---------liveTyping
	def RunCMD(self, cmd: str):
		if not cmd:
			return

		cmd = cmd.strip()

		##expr - 
		if cmd.lower().startswith("expr-"):
			expr = cmd[5:].strip()
			return None#self.Expr(expr)


		cmd = self._cleanArgs(cmd)

		try:
			run(f"op('{self.ownerComp}').{cmd}", self)
			return 1
			
		except Exception as e:
			print(f"TinyUI command failed: {cmd}")
			print(e)
			return None

	def _cleanArgs(self, input: str):
		input = input.strip()

		if input.lower() in ("clear", "clear()"):
			return "Clear()"

		if input.lower() in ("remove", "remove()"):
			return "Remove()"

		if input.startswith("Add"):
			return input

		if input.startswith("add"):
			return input[:1].upper() + input[1:]

		commands = {
			"slider": "AddSlider",
			"menu": "AddMenu",
			"button": "AddButtons",
			"buttons": "AddButtons",
			"stepper": "AddStepper",
			"divider": "AddDivider",
			"emptyline": "AddEmptyLine",
			"littleanimation": "AddLittleAnimation",
			"bitpattern": "AddBitPattern",
		}

		name = input.split("(", 1)[0].strip().lower()

		if name in commands:
			replacement = commands[name]

			if "(" in input:
				args = input[input.find("("):]
				return f"{replacement}{args}"

			return f"{replacement}()"

		if "(" in input:
			name, args = input.split("(", 1)
			name = name.strip()

			if name:
				name = name[0].upper() + name[1:]
				return f"Add{name}({args}"

		input = input[:1].upper() + input[1:]
		return f"Add{input}"
	




##----------------initialize
	def onInitTD(self):
		self._rebuildLayout()
		self._rebuildMidiLookupsFromLayout()
		run(lambda: self.tui.cook(force = True), delayFrames = 1)
