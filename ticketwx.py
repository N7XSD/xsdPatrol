"""
wxPython (GUI) interface for xsdPatrol time keeping module
"""

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements

import logging
import wx

import common
import commonwx


class SelectTicket(commonwx.CommonFrame):
    """
    Window used to select a ticket
    """

    def __init__(self, parent, cmn, title):
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init ticketwx.SelectTicket")

        self.Show()

    def build_selection_list(self, s_list):
        """Data, pretty data"""

        # Begin test data creation
        list_of_stuff = [
            ("Closed", "2025-04-01 08:00", "one"),
            ("Closed", "2025-04-01 09:00", "two"),
            ("Closed", "2025-04-01 10:00", "three"),
            ("", "2025-04-01 11:00", "four"),
            ("", "2025-04-01 12:00", "five"),
            ("", "2025-04-01 13:00", "six"),
            ("", "2025-04-01 14:00", "seven"),
            ("", "2025-04-01 15:00", "eight"),
            ("", "2025-04-01 16:00", "nine"),
            ("", "2025-04-01 17:00", "last")]
        s_list.AppendColumn("State", wx.LIST_FORMAT_LEFT, 64)
        s_list.AppendColumn("Time Opened", wx.LIST_FORMAT_LEFT, 128)
        s_list.AppendColumn("Description", wx.LIST_FORMAT_LEFT, 256)
        for i in list_of_stuff:
            index = s_list.InsertItem(s_list.GetItemCount(), i[0])
            for j, j_text in enumerate(i[1:]):
                s_list.SetItem(index, j+1, j_text)
        # End test data creation

    def create_menu_bar(self):
        """No menu bar"""
        return None

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""
        # Static text

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        self.selection_list = wx.ListCtrl(self.pnl, style=wx.LC_REPORT)
        include_closed_ctrl = wx.CheckBox(self.pnl,
            label="Include closed")
        refresh_button = wx.Button(self.pnl, wx.ID_ANY, "Refresh")
        cancel_button = wx.Button(self.pnl, wx.ID_CANCEL)
        new_button = wx.Button(self.pnl, wx.ID_NEW)
        open_button = wx.Button(self.pnl, wx.ID_ANY, "Open")

        self.build_selection_list(self.selection_list)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_new, new_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_open, open_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_refresh, refresh_button)

        # BOX 0
        # Selection List
        sizer_selection_list = wx.BoxSizer(wx.HORIZONTAL)
        sizer_selection_list.Add(self.selection_list, 1, wx.EXPAND)

        sizer_box0_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box0_main.Add(sizer_selection_list, 1, wx.EXPAND)

        # BOX n - 1
        # Choices
        sizer_choice = wx.BoxSizer(wx.HORIZONTAL)
        sizer_choice.Add(include_closed_ctrl, 0)

        # BOX n
        # Create a sizer to hold the buttons
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_button.Add(refresh_button, 0)

        sizer_button.AddStretchSpacer()
        sizer_button.Add(cancel_button, 0)
        sizer_button.Add(new_button, 0)
        sizer_button.Add(open_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_box0_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_choice, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_cancel(self, _event):
        """Cancel the window"""

    def on_new(self, _event):
        """Create a new ticket"""

    def on_open(self, _event):
        """Open an existing ticket"""

    def on_refresh(self, _event):
        """Refresh the window"""


class SelectEvent(commonwx.CommonFrame):
    """
    Window used to select an event
    """

    def __init__(self, parent, cmn, title):
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init ticketwx.SelectEvent")

        self.Show()

    def build_selection_list(self, s_list):
        """Data, pretty data"""

        # Begin test data creation
        list_of_stuff = [
            ("2025-04-01 08:00", "one"),
            ("2025-04-01 09:00", "two"),
            ("2025-04-01 10:00", "three"),
            ("2025-04-01 11:00", "four"),
            ("2025-04-01 12:00", "five"),
            ("2025-04-01 13:00", "six"),
            ("2025-04-01 14:00", "seven"),
            ("2025-04-01 15:00", "eight"),
            ("2025-04-01 16:00", "nine"),
            ("2025-04-01 17:00", "last")]
        s_list.AppendColumn("Time", wx.LIST_FORMAT_LEFT, 128)
        s_list.AppendColumn("Description", wx.LIST_FORMAT_LEFT, 256)
        for i in list_of_stuff:
            index = s_list.InsertItem(s_list.GetItemCount(), i[0])
            for j, j_text in enumerate(i[1:]):
                s_list.SetItem(index, j+1, j_text)
        # End test data creation

    def create_menu_bar(self):
        """No menu bar"""
        return None

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""
        # Static text

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        self.selection_list = wx.ListCtrl(self.pnl, style=wx.LC_REPORT)
        self.build_selection_list(self.selection_list)
        filter_button = wx.Button(self.pnl, wx.ID_ANY, "Filter")
        refresh_button = wx.Button(self.pnl, wx.ID_ANY, "Refresh")
        cancel_button = wx.Button(self.pnl, wx.ID_CANCEL)
        ok_button = wx.Button(self.pnl, wx.ID_OK)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_filter, filter_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_ok, ok_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_refresh, refresh_button)

        # BOX 0
        # Selection List
        sizer_selection_list = wx.BoxSizer(wx.HORIZONTAL)
        sizer_selection_list.Add(self.selection_list, 1, wx.EXPAND)

        sizer_box0_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box0_main.Add(sizer_selection_list, 1, wx.EXPAND)

        # BOX n
        # Create a sizer to hold the buttons
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_button.Add(filter_button, 0)
        sizer_button.Add(refresh_button, 0)

        sizer_button.AddStretchSpacer()
        sizer_button.Add(cancel_button, 0)
        sizer_button.Add(ok_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_box0_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_cancel(self, _event):
        """Cancel the window"""

    def on_filter(self, _event):
        """Change the data filter"""

    def on_ok(self, _event):
        """The input is OK"""

    def on_refresh(self, _event):
        """Refresh the window"""


if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    stns = common_stuff.stns
    app = wx.App(False)
    frame1 = SelectTicket(None, common_stuff, "Select Ticket")
    frame2 = SelectEvent(None, common_stuff, "Select Event")
    app.MainLoop()
