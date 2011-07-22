from __future__ import generators, print_function
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot, QPointF

from cell import CellSkin

class TextCell(CellSkin):

	typeInfo = "Some text to commence with the reading. May be file backed, may be not."

	def __init__(self, cellId, text=None, cons=None, props=None, editable=True):
		CellSkin.__init__(self, cellId, text or "", cons, props)
		self.initData = self._data
		self.editable = editable

	def execute(self):
		pass

	def placeChildren(self, space):
		if self.editable: Text = QtGui.QGraphicsTextItem
		else: Text = QtGui.QGraphicsSimpleTextItem
		if self.dataInline:
			text = Text(self.initData, self.skin)
		elif os.path.exists(self.data):
			filey = file(self.initData, "r")
			conts = filey.read()
			filey.close()
			text = Text(conts, self.skin)
		self.initData = None
		if self.editable:
			qt = QtCore.Qt
			text.setTextInteractionFlags(qt.TextEditorInteraction|qt.TextBrowserInteraction)
			text.document().contentsChanged.connect(self.updateRect)
			text.document().contentsChanged.connect(space.chugDraw)
			text.document().setDocumentMargin(5)

	
	def createData(self, scene):
		# our default is all we need
		pass

	def getText(self):
		if self.editable:
			return self.getChild().toPlainText()
		return self.getChild().text()
	
	def setText(self, text):
		wid = self.getChild()
		if self.editable: wid.setPlainText(text)
		else: wid.setText(text)

	def beforeSkinDestroyHook(self):
		self.initData = self.data

	@property
	def data(self):
		if self.skin:
			return str(self.getText())
		return self.initData
	@data.setter
	def data(self, val):
		if self.skin:
			self.setText(val)
		else:
			self.initData = val

	@pyqtSlot()
	def edit(self):
		if self.editable:
			text = self.getChild()
			text.setFocus()
