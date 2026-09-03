"""
wxPython (GUI) for SCS Patrol DB
"""

import getpass
import logging
import platform
import wx

import common
import commonwx
import db_dispatch
import db_member
import wx_member
import wx_member_list
import wx_time_import

class PatrolDBMain(commonwx.CommonFrame):
    """
    Frame for Patrol DB
    """

    def __init__(self, parent, cmn):
        super().__init__(parent, cmn)
        self.cmn = cmn
        self.pnl = wx.Panel(self)
        logging.debug("Init wx_patrol.PatrolBMain")
##      self.ddb_reports = common.DispatchDbReports()
##      self.html_print = wx.html.HtmlEasyPrinting(parentWindow=self)

        try:
            import db_patrol
            self.cmn.patrol_db = db_patrol.PatrolDB(self.cmn)
        except Exception as e:
            # No point in going further without PatrolDB.
            logging.debug(f"Can not access Patrol DB; {e}")
            dlg = wx.MessageDialog(None,
                f"Can not access Patrol DB.  Terminating applications.\n{e}",
                style=wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP,
                caption="xsdPatrol")
            dlg.ShowModal()
            logging.info("Terminating application.")
            wx.Exit()

        self.SetTitle("xsdPatrol")

        # Create the menubar
        menu_bar = self.create_menu_bar()
        self.SetMenuBar(menu_bar)

        # Layout sizers
        sizer_main = self.create_sizer_main()
        self.pnl.SetSizer(sizer_main)
        self.pnl.SetAutoLayout(1)
        sizer_main.Fit(self)

        self.SetMinSize(wx.Size(256, 256))
        self.Show()

    def create_sizer_common_buttons(self):
        """Create a size for Common task task buttons"""

        # Static text
        label_common = wx.StaticText(self.pnl,
            label="Common Tasks")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        member_list_button = wx.Button(self.pnl, wx.ID_ANY,
            "Member List")

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_member_list,
            member_list_button)

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(label_common, 0)
        this_sizer.Add(member_list_button, 0)
        return this_sizer

    def create_sizer_time_import(self):
        """Create a size for time task buttons"""

        # Static text
        label_time = wx.StaticText(self.pnl,
            label="Time Keeping Tasks")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        time_button = wx.Button(self.pnl, wx.ID_ANY,
            "Time Import")

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_time, time_button)

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(label_time, 0)
        this_sizer.Add(time_button, 0)
        return this_sizer

    def create_sizer_admin_buttons(self):
        """Create a size for Admin task buttons"""

        # Static text
        label_admin = wx.StaticText(self.pnl,
            label="Admin Tasks")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        import_button = wx.Button(self.pnl, wx.ID_ANY,
            "Import from MemberDB")

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
#       label_db_patrol = wx.StaticText(self.pnl,
#           label=f"Patrol DB:  {self.cmn.patrol_db_open_info}")
#       label_db_dispatch = wx.StaticText(self.pnl,
#           label=f"Dispatch DB:  {self.cmn.dispatch_db_open_info}")
#       label_db_member = wx.StaticText(self.pnl,
#           label=f"Member DB:  {self.cmn.member_db_open_info}")

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(label_user_name)
        this_sizer.Add(label_platform)
#       this_sizer.Add(label_db_patrol)
#       this_sizer.Add(label_db_dispatch)
#       this_sizer.Add(label_db_member)
        return this_sizer

    def create_sizer_main(self):
        """The main sizer holds everything the user will interact with"""

        # Use a vertical sizer to stack our window
        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(self.create_sizer_common_buttons(),
            1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        this_sizer.Add(self.create_sizer_time_import(),
            1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        this_sizer.Add(self.create_sizer_admin_buttons(),
            1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        this_sizer.Add(self.create_sizer_info(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        this_sizer.Add(self.create_sizer_bottom_buttons(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return this_sizer

    def on_member_list(self, _event):
        """Import data from MemberDB"""
        wx_member_list.MemberList(self, self.cmn)

    def on_import(self, _event):
        """Import data from MemberDB"""
        wx_member.Import(self, self.cmn)

    def on_time(self, _event):
        """Import data from MemberDB"""
        wx_time_import.TimeImport(self, self.cmn)

if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    stns = common_stuff.stns
    app = wx.App(False)
    frame = PatrolDBMain(None, common_stuff)
    app.MainLoop()
