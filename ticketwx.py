"""
wxPython (GUI) interface for xsdPatrol time keeping module
"""

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements

import logging
import wx

import common
import commonwx


class SelectEvent(commonwx.CommonFrame):
    """
    Window used to select an event
    """

    def __init__(self, parent, cmn, title):
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init ticketwx.SelectEvent")

        self.Show()

    def create_menu_bar(self):
        """Create the menu bar"""

        # Create MenuItems
        # Note: About and Exit are moved to the application menu in macOS
        about_mitem = wx.MenuItem(None, wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.on_about, about_mitem)

        exit_mitem = wx.MenuItem(None, wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_mitem)

        # File menu
        file_menu = wx.Menu()
#       file_menu.AppendSeparator()
        file_menu.Append(exit_mitem)

        # Help menu
        help_menu = wx.Menu()
        help_menu.Append(about_mitem)

        # Create the menubar
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")

        return menu_bar

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""
        # Static text

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        selection_list = wx.ListCtrl(self.pnl)
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
        sizer_selection_list.Add(selection_list, 1, wx.EXPAND)

        sizer_box0_main = wx.BoxSizer(wx.VERTICAL)
#       sizer_box0_main.Add(label_start_date)
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
    frame = SelectEvent(None, common_stuff, "Select")
    app.MainLoop()
