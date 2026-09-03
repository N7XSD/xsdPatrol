"""
wxPython (GUI) for creating a grid with a member list
"""

import logging
import wx
import wx.grid

import common
import commonwx
import wx_member_edit

class MemberList(commonwx.CommonFrame):
    """
    Frame for listing members
    """

    def __init__(self, parent, cmn):
        super().__init__(parent, cmn)
        self.pnl = wx.Panel(self)
        logging.debug("Init wx_member_list.MemberList")

        self.cmn = cmn
        self.title_font = wx.Font(wx.FontInfo(16).Bold())
        self.data_font = wx.Font(
            wx.FontInfo().Family(wx.FONTFAMILY_TELETYPE))
        self.members = self.cmn.patrol_db.get_members()
        self.SetTitle("Members")

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

    def create_sizer_grid(self):
        """The grid displays our imported data"""

        field_headers = [
            "Member ID",
            "Logging ID",
            "Last Name",
            "First Name",
            "Nickname"]

        self.member_grid = wx.grid.Grid(self.pnl, -1)
        self.member_grid.CreateGrid(len(self.members), len(field_headers))
        self.member_grid.EnableEditing(False)
        self.member_grid.HideRowLabels()
        self.member_grid.SetDefaultCellFont(self.data_font)
        self.member_grid.SetSelectionMode(wx.grid.Grid.GridSelectRows)
        self.member_grid.SetUseNativeColLabels()
#       self.member_grid.UseNativeColHeader()
        self.member_grid.SetColFormatNumber(0)
        for i in range(len(field_headers)):
            self.member_grid.SetColLabelValue(i, field_headers[i])
        for i in range(len(self.members)):
            self.member_grid.SetCellValue(i, 0,
                str(self.members[i].member_id))
            self.member_grid.SetCellValue(i, 1,
                str(self.members[i].user_name_logdb))
            self.member_grid.SetCellValue(i, 2,
                str(self.members[i].surname))
            self.member_grid.SetCellValue(i, 3,
                str(self.members[i].given_name))
            self.member_grid.SetCellValue(i, 4,
                str(self.members[i].nickname))
        self.member_grid.AutoSize()

        # Bind widgets to methods
        self.pnl.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
            self.on_select_member, self.member_grid)

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(self.member_grid, 0, wx.EXPAND)

        return this_sizer

    def create_sizer_bottom_buttons(self):
        """Create a sizer to hold the buttons"""

        # Static text

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        exit_button = wx.Button(self.pnl, wx.ID_EXIT)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_exit, exit_button)

        this_sizer = wx.BoxSizer(wx.HORIZONTAL)
        this_sizer.AddStretchSpacer()
        this_sizer.Add(exit_button, 0)

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

    def on_exit(self, _event):
        """Exit"""
        self.Close(True)  # Close the frame

    def on_select_member(self, _event):
        """Edit the member we've selected"""
        table_row = _event.GetRow()
        member_id = self.member_grid.GetCellValue(_event.GetRow(), 0)
        for m in self.members:
            if int(m.member_id) == int(member_id):
                wx_member_edit.MemberEdit(self, self.cmn, m,
                    self.cmn.patrol_db)
