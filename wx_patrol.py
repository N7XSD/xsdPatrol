"""
wxPython (GUI) for SCS Patrol DB
"""

import getpass
import logging
import platform
import wx

import common
import commonwx

class PatrolDBMain(commonwx.CommonFrame):
    """
    Frame for Patrol DB
    """

    def __init__(self, parent, cmn, title):
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init wx_patrol.PatrolBMain")
#       self.reports = common.DispatchDbReports()
#       self.html_print = wx.html.HtmlEasyPrinting(parentWindow=self)

        self.Show()

    def create_sizer_heading(self):
        """Create a sizer to hold some text at the top of our frame"""

        # Static text
        label_common_frame = wx.StaticText(self.pnl,
            label="Maybe some intersting buttons.  Maybe.")

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(label_common_frame)
        return this_sizer

    def create_sizer_info(self):
        """Static information for the user"""

        hostname = platform.node()
        pform = platform.platform()
        user_name = getpass.getuser()

        label_platform = wx.StaticText(self.pnl,
            label=f"Platform:  {pform}")
        label_user_name = wx.StaticText(self.pnl,
            label=f"User:  {user_name}@{hostname}")
        label_db_patrol = wx.StaticText(self.pnl,
            label=f"Patrol DB:  {self.cmn.patrol_db_open_info}")
        label_db_dispatch = wx.StaticText(self.pnl,
            label=f"Dispatch DB:  {self.cmn.dispatch_db_open_info}")
        label_db_member = wx.StaticText(self.pnl,
            label=f"Member DB:  {self.cmn.member_db_open_info}")

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(label_user_name)
        this_sizer.Add(label_platform)
        this_sizer.Add(label_db_patrol)
        this_sizer.Add(label_db_dispatch)
        this_sizer.Add(label_db_member)
        return this_sizer

    def create_sizer_main(self):
        """The main sizer holds everything the user will interact with"""

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(self.create_sizer_heading(),
            1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(self.create_sizer_info(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(self.create_sizer_bottom_buttons(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    stns = common_stuff.stns
    app = wx.App(False)
    frame = PatrolDBMain(None, common_stuff,
        "xsdPatrol")
#    frame.SetPosition(stns.get_window_pos_time())
#    frame.SetSize(stns.get_window_size_time())
    app.MainLoop()
