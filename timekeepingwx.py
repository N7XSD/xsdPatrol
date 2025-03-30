"""
wxPython (GUI) interface for xsdPatrol time keeping module
"""

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements

import datetime
import logging
import wx
#import wx.adv
#import wx.grid

#import activitywx
#import peoplewx
import common
#import data
#import settings


class TimekeepingMain(wx.Frame):
    """
    Main window for time keeping module
    """

    def __init__(self, parent, cmn, title):
        wx.Frame.__init__(self, parent, title=title)
        logging.debug("Init timekeepingwx.TimekeepingMain")
        self.pnl = wx.Panel(self)
        self.cmn = cmn
        working_d = (self.cmn.app_start_time_dt
            - datetime.timedelta(weeks=1)).date()
        self.cmn.get_last_work_week(working_d)

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
        self.SetMenuBar(menu_bar)

        # Static text
        label_start_date = wx.StaticText(self.pnl, label="Test Date")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        ctrl_start_date = wx.TextCtrl(self.pnl,
            style=wx.TE_READONLY)
        exit_button = wx.Button(self.pnl, wx.ID_EXIT)

        ctrl_start_date.SetValue(working_d.isoformat())

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_exit, exit_button)

        # BOX 0
        # Headings
        sizer_heading_date = wx.BoxSizer(wx.HORIZONTAL)
        sizer_heading_date.Add(ctrl_start_date, 1)

        sizer_box0_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box0_main.Add(label_start_date)
        sizer_box0_main.Add(sizer_heading_date, 1, wx.EXPAND)

        # BOX n
        # Create a sizer to hold the buttons
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)

        sizer_button.AddStretchSpacer()
        sizer_button.Add(exit_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_box0_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.widget_border)
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.widget_border)

        # Layout sizers
        self.pnl.SetSizer(sizer_main)
        self.pnl.SetAutoLayout(1)
        sizer_main.Fit(self)

        self.Show()

    def on_about(self, _event):
        """Create a message dialog box"""
        dlg = wx.MessageDialog(self,
            "Timekeeping Application",
            "About Patrol Timekeeping", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished

    def on_exit(self, _event):
        """Exit"""
        logging.debug("Exit TimekeepingMain")
        self.Close(True)  # Close the frame


if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    stns = common_stuff.stns
    app = wx.App(False)
    frame = TimekeepingMain(None, common_stuff,
        "Patrol Timekeeping Management")
#    frame.SetPosition(stns.initial_window_position)
#    frame.SetSize(stns.initial_window_size)
    app.MainLoop()
