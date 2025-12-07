# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         TreeCtrlComboPopup.py
# Purpose:      Popup control containing a TreeCtrl.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: TreeCtrlComboPopup.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx

class TreeCtrlComboPopup(wx.ComboPopup):
    "Popup control containing a TreeCtrl"

    # Overridden ComboPopup methods

    def Init(self):
        "Initialize the internal variables"
        self.value = None
        self.curitem = None

    def Create(self, parent):
        "Must be implemented to create the popup control"
        self.tree = wx.TreeCtrl(parent, style=wx.TR_HIDE_ROOT
                                |wx.TR_HAS_BUTTONS
                                |wx.TR_SINGLE
                                |wx.TR_LINES_AT_ROOT
                                |wx.SIMPLE_BORDER)
        # f32: not in list of supported options |wx.SIMPLE_BORDER)
        # Events
        # f32: how did this work? Does it still?
        # self.tree.Bind(wx.EVT_MOTION, self.OnMotion)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        
    def GetControl(self):
        "Return pointer to the associated control created in Create"
        return self.tree

    def GetStringValue(self):
        "Return string representation of the value"
        if self.value:
            return self.tree.GetItemText(self.value)
        return ""

    def OnPopup(self):
        "Do special processing when popup is shown"
        if self.value:
            # Select the current value and make it visible
            self.tree.EnsureVisible(self.value)
            self.tree.SelectItem(self.value)

    def SetStringValue(self, value):
        "Receive string value changes from wxComboCtrl"
        # This assumes that item strings are unique...
        # And it's true for the encodings use :)
        root = self.tree.GetRootItem()
        if not root:
            return
        else:
            return
        found = self.FindItem(root, value)
        if found:
            self.value = found
            self.tree.SelectItem(found)

    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        "Return adjusted size for the popup control"
        # Maybe I'll need to customize this...
        return wx.Size(minWidth, min(200, maxHeight))
                       
    # Auxiliar methods
    
    def FindItem(self, parentItem, text):
        "Search for a text item on the tree"
        '''
        item, cookie = self.tree.GetFirstChild(parentItem)
        while item:
            if self.tree.GetItemText(item) == text:
                return item
            if self.tree.ItemHasChildren(item):
                item = self.FindItem(item, text)
            item, cookie = self.tree.GetNextChild(parentItem, cookie)
        return wx.TreeItemId();
        '''
        return True

    def AddItem(self, value, parent=None):
        "Add an item to the tree"
        if not parent:
            root = self.tree.GetRootItem()
            if not root:
                # Any text can be used for the root
                root = self.tree.AddRoot("<hidden root>")
            parent = root

        item = self.tree.AppendItem(parent, value)
        return item

    def OnMotion(self, evt):
        "Events when the mouse moves over the combo"
        # Have the selection follow the mouse, like in a real combobox
        item, flags = self.tree.HitTest(evt.GetPosition())
        if item and flags & wx.TREE_HITTEST_ONITEMLABEL:
            self.tree.SelectItem(item)
            self.curitem = item
        evt.Skip()

    def OnLeftDown(self, evt):
        "Events when the mouse clicks over the combo"
        # Do the combobox selection
        item, flags = self.tree.HitTest(evt.GetPosition())
        if item and flags & wx.TREE_HITTEST_ONITEMLABEL:
            self.curitem = item
            self.value = item
            self.Dismiss()
        evt.Skip()
