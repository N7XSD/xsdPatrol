"""
wxPython (GUI) for creating a grid with a member list
"""

import logging
import wx
import wx.grid

import common
import commonwx
import db_patrol

class MemberList(commonwx.CommonFrame):
    """
    Frame for listing members
    """

    def __init__(self, parent, cmn):
        self.cmn = cmn
        wx.Frame.__init__(self, parent)
        self.pnl = wx.Panel(self)
        logging.debug("Init wx_member_list.MemberList")

        self.pdb = db_patrol.PatrolDB(self.cmn)
        self.members = self.pdb.get_members()

        # Create the menubar
        menu_bar = self.create_menu_bar()
        self.SetMenuBar(menu_bar)

        # Layout sizers
        sizer_main = self.create_sizer_main()
        self.pnl.SetSizer(sizer_main)
        self.pnl.SetAutoLayout(1)
        sizer_main.Fit(self)

        self.SetTitle("Members")
        self.SetMinSize(wx.Size(256, 256))
        self.Show()

    def create_sizer_grid(self):
        """The grid displays our imported data"""

        field_headers = [
            "Member ID",
            "Logging ID",
            "Last Name",
            "First Name",
            "Nickname"]

        member_grid = wx.grid.Grid(self.pnl, -1)
        member_grid.CreateGrid(len(self.members), len(field_headers))
        member_grid.HideRowLabels()
        member_grid.SetColFormatNumber(0)
        for i in range(len(field_headers)):
            member_grid.SetColLabelValue(i, field_headers[i])
        for i in range(len(self.members)):
            member_grid.SetReadOnly(i, 0)
            member_grid.SetCellValue(i, 0,
                str(self.members[i].member_id))
            member_grid.SetReadOnly(i, 1)
            member_grid.SetCellValue(i, 1,
                str(self.members[i].user_name_logdb))
            member_grid.SetReadOnly(i, 2)
            member_grid.SetCellValue(i, 2,
                str(self.members[i].surname))
            member_grid.SetReadOnly(i, 3)
            member_grid.SetCellValue(i, 3,
                str(self.members[i].given_name))
            member_grid.SetReadOnly(i, 4)
            member_grid.SetCellValue(i, 4,
                str(self.members[i].nickname))
        member_grid.AutoSize()

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(member_grid, 0)

        return this_sizer

    def create_sizer_heading(self):
        """Create a sizer to hold some text at the top of our frame"""

        # Static text
        r = len(self.members)
        label_common_frame = wx.StaticText(self.pnl,
            label=f"{r} records displayd.")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.

        # Bind widgets to methods

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(label_common_frame, 0)

        return this_sizer

    def create_sizer_main(self):
        """The main sizer holds everything the user will interact with"""

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(self.create_sizer_heading(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(self.create_sizer_grid(),
            1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(self.create_sizer_bottom_buttons(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_cancel(self, _event):
        """Cancel"""
        self.Destroy()  # Close the frame

    def on_exit(self, _event):
        """Exit"""
        self.Close()  # Close the frame
