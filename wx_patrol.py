"""
wxPython (GUI) for SCS Patrol DB
"""

import getpass
import logging
import platform
import wx

import common
import commonwx
import wx_member

class PatrolDBMain(commonwx.CommonFrame):
    """
    Frame for Patrol DB
    """

    def __init__(self, parent, cmn):
        commonwx.CommonFrame.__init__(self, parent, cmn)
        logging.debug("Init wx_patrol.PatrolBMain")
##      self.reports = common.DispatchDbReports()
##      self.html_print = wx.html.HtmlEasyPrinting(parentWindow=self)

        self.SetTitle("xsdPatrol")
        self.Show()

    def create_sizer_admin_buttons(self):
        """Create a size for Admin task buttons"""

        # Static text
        label_admin = wx.StaticText(self.pnl,
            label="Administration")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        import_button = wx.Button(self.pnl, wx.ID_ANY,
            "Import from Dispatch Log")

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_import, import_button)

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(label_admin, 0)
        this_sizer.Add(import_button, 0)
        return this_sizer

    def create_sizer_info(self):
        """Static information for the user"""

        hostname = platform.node()
        pform = platform.platform()
        user_name = getpass.getuser()

        label_user_name = wx.StaticText(self.pnl,
            label=f"User:  {user_name}@{hostname}")
        label_platform = wx.StaticText(self.pnl,
            label=f"Platform:  {pform}")
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
        sizer_main.Add(self.create_sizer_admin_buttons(),
            1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(self.create_sizer_info(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(self.create_sizer_bottom_buttons(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_import(self, _event):
        """Import data from MemberDB"""

        import_frame = wx_member.Import(self, self.cmn)

if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    stns = common_stuff.stns
    app = wx.App(False)
    frame = PatrolDBMain(None, common_stuff)
    app.MainLoop()
