"""
wxPython (GUI) for accessing MemberDB
"""

import logging
import wx
import wx.grid

import common
import commonwx

class Import(commonwx.CommonFrame):
    """
    Frame for importing data from MemberDB
    """

    def __init__(self, parent, cmn):
        self.cmn = cmn
        wx.Frame.__init__(self, parent)
        self.pnl = wx.Panel(self)
        logging.debug("Init wx_member.Import")

#      Checks that may need human attention
#          dl_stat_code is a valide US state or Canadian Province/Territory
        self.members = self.cmn.member_db.get_members()

        # Create the menubar
        menu_bar = self.create_menu_bar()
        self.SetMenuBar(menu_bar)

        # Layout sizers
        sizer_main = self.create_sizer_main()
        self.pnl.SetSizer(sizer_main)
        self.pnl.SetAutoLayout(1)
        sizer_main.Fit(self)

        self.SetTitle("Import from MemberDB")
        self.SetMinSize(wx.Size(256, 256))
        self.Show()

    def create_sizer_grid(self):
        """The grid displays our imported data"""

        field_headers = [
            "ID",
            "Logging User_ID",
            "Last Name",
            "First Name",
            "PrefName",
            "Email",
            "Home Phone",
            "Cell Phone",
            "MAddress",
            "City",
            "State",
            "ZIP",
            "Notes",
            "Birthday",
            "Renter?",
            "LeaseExpDate",
            "AssociationNo",
            "License No",
            "DL Expiry Date",
            "DL State",
            "Deceased?",
            "DHRdate"]

        member_grid = wx.grid.Grid(self.pnl, -1)
        member_grid.CreateGrid(len(self.members), len(field_headers))
        member_grid.HideRowLabels()
        member_grid.SetColFormatNumber(0)
        for i in range(len(field_headers)):
            member_grid.SetColLabelValue(i, field_headers[i])
        for i in range(len(self.members)):
            member_grid.SetReadOnly(i, 0)
            member_grid.SetCellValue(i, 0, str(self.members[i].member_id))
            member_grid.SetCellValue(i, 1, str(self.members[i].user_name_logdb))
            member_grid.SetCellValue(i, 2, str(self.members[i].surname))
            member_grid.SetCellValue(i, 3, str(self.members[i].given_name))
            member_grid.SetCellValue(i, 4, str(self.members[i].nickname))
            member_grid.SetCellValue(i, 5, "")
            if self.members[i].email_address:
                member_grid.SetCellValue(i, 5,
                    str(self.members[i].email_address[0].email_addr))
            for j in self.members[i].telephone_number:
               if j.phone_type == 2:	# Home phone
                   member_grid.SetCellValue(i, 6, str(j.phone_number))
               if j.phone_type == 1:	# Mobile phone
                   member_grid.SetCellValue(i, 7, str(j.phone_number))
            if self.members[i].physical_address:
                member_grid.SetCellValue(i, 8,
                    f"{self.members[i].physical_address[0].street_number} "
                    f"{self.members[i].physical_address[0].street_name}")
                member_grid.SetCellValue(i, 9,
                    str(self.members[i].physical_address[0].city_name))
                member_grid.SetCellValue(i, 10,
                    str(self.members[i].physical_address[0].state_code))
                member_grid.SetCellValue(i, 11,
                    str(self.members[i].physical_address[0].postal_code))
                member_grid.SetCellValue(i, 14,
                    str(self.members[i].physical_address[0].renter))
                member_grid.SetCellValue(i, 15,
                    str(self.members[i].physical_address[0].lease_expiry_date))
                member_grid.SetCellValue(i, 16,
                    str(self.members[i].physical_address[0].scscai_number))
            if self.members[i].member_notes:
                member_grid.SetCellValue(i, 12,
                    str(self.members[i].member_notes[0].member_note))
            member_grid.SetCellValue(i, 13, str(self.members[i].birthdate))
            member_grid.SetCellValue(i, 17, str(self.members[i].dl_number))
            member_grid.SetCellValue(i, 18, str(self.members[i].dl_expiry_date))
            member_grid.SetCellValue(i, 19, str(self.members[i].dl_state_code))
            member_grid.SetCellValue(i, 20, str(self.members[i].deceased))
            if self.members[i].dl_history:
                member_grid.SetCellValue(i, 21,
                    str(self.members[i].dl_history[0].dl_history_date))
#       member_grid.AutoSize()

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(member_grid, 0)

        return this_sizer

    def create_sizer_heading(self):
        """Create a sizer to hold some text at the top of our frame"""

        # Static text
        r = len(self.members)
        label_common_frame = wx.StaticText(self.pnl,
            label=f"{r} records read.")

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


#       active_members = self.cmn.member_db.get_active_members()
#       sorted_members = dict(sorted(active_members.items()))
#       for i_key, i_value in sorted_members.items():
#           print(f"{i_key}: {i_value}")
