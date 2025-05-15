"""
wxPython (GUI) frame for xsdPatrol
"""

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements

#import datetime
import logging
import wx

import common


class CommonFrame(wx.Frame):
    """
    Base class for xsdPatrol frames
    """

    def __init__(self, parent, cmn, title):
        wx.Frame.__init__(self, parent, title=title)
        self.SetMinSize(wx.Size(512, 256))
        self.pnl = wx.Panel(self)
        self.cmn = cmn

        # Create the menubar
        menu_bar = self.create_menu_bar()
        self.SetMenuBar(menu_bar)

        # Layout sizers
        sizer_main = self.create_sizer_main()
        self.pnl.SetSizer(sizer_main)
        self.pnl.SetAutoLayout(1)
        sizer_main.Fit(self)

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
        label_common_frame = wx.StaticText(self.pnl, label="Common Frame")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        exit_button = wx.Button(self.pnl, wx.ID_EXIT)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_exit, exit_button)

        # BOX 0
        # Headings
        sizer_common_frame = wx.BoxSizer(wx.HORIZONTAL)
        sizer_box0_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box0_main.Add(label_common_frame)

        # BOX n
        # Create a sizer to hold the buttons
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)

        sizer_button.AddStretchSpacer()
        sizer_button.Add(exit_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_box0_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_about(self, _event):
        """Create a message dialog box"""
        dlg = wx.MessageDialog(self,
            "About text.",
            "About Box Title", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished

    def on_exit(self, _event):
        """Exit"""
        self.Close(True)  # Close the frame


if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    stns = common_stuff.stns
    app = wx.App(False)
    frame = CommonFrame(None, common_stuff,
        "Base for xsdPatrol")
#    frame.SetPosition(stns.get_window_pos_time())
#    frame.SetSize(stns.get_window_size_time())
    app.MainLoop()
