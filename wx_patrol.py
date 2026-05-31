"""
wxPython (GUI) for SCS Patrol DB
"""

import getpass
import logging
import platform
import wx

import common
import commonwx

class MemberDBMain(commonwx.CommonFrame):
    """
    Frame for Member DB
    """

    def __init__(self, parent, cmn, title):
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init memberwx.MemberDBMain")
#       self.reports = common.DispatchDbReports()
#       self.html_print = wx.html.HtmlEasyPrinting(parentWindow=self)

        self.Show()

    def create_sizer_main(self):
        """The main sizer holds everything the user will interact with"""

        # Static text
        label_common_frame = wx.StaticText(self.pnl,
            label="Maybe some intersting buttons.  Maybe.")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        cancel_button = wx.Button(self.pnl, wx.ID_CANCEL)
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
        sizer_button.Add(cancel_button, 0)
        sizer_button.Add(exit_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_box0_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(self.create_sizer_info(), 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

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

if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    stns = common_stuff.stns
    app = wx.App(False)
    frame = MemberDBMain(None, common_stuff,
        "xsdPatrol")
#    frame.SetPosition(stns.get_window_pos_time())
#    frame.SetSize(stns.get_window_size_time())
    app.MainLoop()
