"""
wxPython (GUI) frame to display or edit basic member data
"""

import datetime
import logging
import wx

import common
import commonwx


class MemberEdit(commonwx.CommonFrame):
    """
    Patrol data editor
    """

    def __init__(self, parent, cmn, item, db):
        super().__init__(parent, cmn)
        self.pnl = wx.Panel(self)
        logging.debug("Init wx_member_edit.MemberEdit")

        self.cmn = cmn
        self.item = item

        self.title_font = wx.Font(wx.FontInfo(16).Bold())
        self.data_font = wx.Font(
            wx.FontInfo().Family(wx.FONTFAMILY_TELETYPE))
        self.label_size = wx.Size(96, 16)
        self.line_gap = 8

        self.member_id = -99
        self.user_name_logdb = ""
        self.surname = ""
        self.given_name = ""
        self.nickname = ""
        self.telephone_number = []
        self.email_address = []
        self.SetTitle("Basic Member Data")

        try:
            self.member_id = item.member_id
            self.user_name_logdb = item.user_name_logdb
            self.surname = item.surname
            self.given_name = item.given_name
            self.nickname = item.nickname
            self.telephone_number = db.get_member_telephone(self.member_id)
            self.email_address = db.get_member_email(self.member_id)
            self.SetTitle(f"Member ID: {self.member_id}")
        except Exception as e:
            print(e)
            # FIXME: Raise something,
            # without data we can't get any farther

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

    def create_sizer_bottom_buttons(self):
        """Create a sizer to hold the buttons"""

        # Static text

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        cancel_button = wx.Button(self.pnl, wx.ID_CANCEL)
        exit_button = wx.Button(self.pnl, wx.ID_EXIT)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_exit, exit_button)
        this_sizer = wx.BoxSizer(wx.HORIZONTAL)
        this_sizer.AddStretchSpacer()
        this_sizer.Add(cancel_button, 0)
        this_sizer.Add(exit_button, 0)

        return this_sizer

    def create_sizer_email(self):
        """This sizer holds a table of email addresses"""

        # Static text
        label_email = wx.StaticText(self.pnl, label="Email:  ",
            style=wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL,
            size=self.label_size)

        field_headers = [
            "Type",
            "Email Address"]

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        display_rows = max(1, len(self.email_address))
        self.email_grid = wx.grid.Grid(self.pnl, -1)
        self.email_grid.CreateGrid(display_rows, len(field_headers))
        self.email_grid.HideRowLabels()
        self.email_grid.SetDefaultCellFont(self.data_font)
        self.email_grid.SetUseNativeColLabels()
#       self.email_grid.UseNativeColHeader()
        self.email_grid.SetColFormatNumber(0)
        for i in range(len(field_headers)):
            self.email_grid.SetColLabelValue(i, field_headers[i])
        for i in range(len(self.email_address)):
            self.email_grid.SetCellValue(i, 0,
                str(self.email_address[i].email_type))
            self.email_grid.SetCellValue(i, 1,
                str(self.email_address[i].email_addr))
        self.email_grid.AutoSize()

        sub_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sub_sizer.Add(label_email, 0, wx.EXPAND | wx.ALL)
        sub_sizer.Add(self.email_grid, 1, wx.EXPAND | wx.ALL)

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(sub_sizer, 0, wx.EXPAND)

        return this_sizer

    def create_sizer_heading(self):
        """Create a sizer to hold some text at the top of our frame"""

        # Static text
        label_heading = wx.StaticText(self.pnl,
            label="Basic Member Data")
        label_heading.SetFont(self.title_font)

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.

        # Bind widgets to methods

        sub_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sub_sizer.AddStretchSpacer()
        sub_sizer.Add(label_heading, 0, wx.EXPAND | wx.ALL)
        sub_sizer.AddStretchSpacer()

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(sub_sizer, 0, wx.EXPAND | wx.ALL)

        return this_sizer

    def create_sizer_member_data(self):
        """The main sizer holds member data and labels"""

        # Static text
        label_member_id = wx.StaticText(self.pnl, label="MemberID:  ",
            style=wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL,
            size=self.label_size)
        label_given_name = wx.StaticText(self.pnl, label="First Name:  ",
            style=wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL,
            size=self.label_size)
        label_nickname = wx.StaticText(self.pnl, label="Nickname:  ",
            style=wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL,
            size=self.label_size)
        label_surname = wx.StaticText(self.pnl, label="Surname:  ",
            style=wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL,
            size=self.label_size)

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        member_id_ctrl = wx.TextCtrl(self.pnl, wx.ID_ANY,
            str(self.member_id), style=wx.TE_READONLY)
        member_id_ctrl.SetFont(self.data_font)
        given_name_ctrl = wx.TextCtrl(self.pnl, wx.ID_ANY,
            str(self.given_name))
        given_name_ctrl.SetFont(self.data_font)
        nickname_ctrl = wx.TextCtrl(self.pnl, wx.ID_ANY,
            str(self.nickname))
        nickname_ctrl.SetFont(self.data_font)
        surname_ctrl = wx.TextCtrl(self.pnl, wx.ID_ANY,
            str(self.surname))
        surname_ctrl.SetFont(self.data_font)

        # Bind widgets to methods

        sub_sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sub_sizer_1.Add(label_member_id, 0, wx.EXPAND | wx.ALL)
        sub_sizer_1.Add(member_id_ctrl, 1, wx.EXPAND | wx.ALL)

        sub_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sub_sizer_2.Add(label_given_name, 0, wx.EXPAND | wx.ALL)
        sub_sizer_2.Add(given_name_ctrl, 1, wx.EXPAND | wx.ALL)

        sub_sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sub_sizer_3.Add(label_nickname, 0, wx.EXPAND | wx.ALL)
        sub_sizer_3.Add(nickname_ctrl, 1, wx.EXPAND | wx.ALL)

        sub_sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sub_sizer_4.Add(label_surname, 0, wx.EXPAND | wx.ALL)
        sub_sizer_4.Add(surname_ctrl, 1, wx.EXPAND | wx.ALL)

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(sub_sizer_1, 0, wx.EXPAND | wx.ALL)
        this_sizer.AddSpacer(self.line_gap)
        this_sizer.Add(sub_sizer_2, 0, wx.EXPAND | wx.ALL)
        this_sizer.AddSpacer(self.line_gap)
        this_sizer.Add(sub_sizer_3, 0, wx.EXPAND | wx.ALL)
        this_sizer.AddSpacer(self.line_gap)
        this_sizer.Add(sub_sizer_4, 0, wx.EXPAND | wx.ALL)

        return this_sizer

    def create_sizer_telephone(self):
        """This sizer holds a table of telephone numbers"""

        # Static text
        label_telephone = wx.StaticText(self.pnl, label="Telephone:  ",
            style=wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL,
            size=self.label_size)

        field_headers = [
            "Type",
            "Country Code",
            "Number",
            "Ext"]

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        display_rows = max(1, len(self.telephone_number))
        self.telephone_grid = wx.grid.Grid(self.pnl, -1)
        self.telephone_grid.CreateGrid(display_rows, len(field_headers))
        self.telephone_grid.HideRowLabels()
        self.telephone_grid.SetDefaultCellFont(self.data_font)
        self.telephone_grid.SetUseNativeColLabels()
#       self.telephone_grid.UseNativeColHeader()
        self.telephone_grid.SetColFormatNumber(0)
        for i in range(len(field_headers)):
            self.telephone_grid.SetColLabelValue(i, field_headers[i])
        for i in range(len(self.telephone_number)):
            self.telephone_grid.SetCellAlignment(i, 1,
                wx.ALIGN_RIGHT, wx.ALIGN_TOP)

            self.telephone_grid.SetCellValue(i, 0,
                str(self.telephone_number[i].phone_type))
            self.telephone_grid.SetCellValue(i, 1,
                str(self.telephone_number[i].phone_country_code))
            self.telephone_grid.SetCellValue(i, 2,
                str(self.telephone_number[i].phone_number))
            ext = self.telephone_number[i].phone_ext
            if ext:
                self.telephone_grid.SetCellValue(i, 3, str(ext))
            else:
                self.telephone_grid.SetCellValue(i, 3, "")
        self.telephone_grid.AutoSize()

        sub_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sub_sizer.Add(label_telephone, 0, wx.EXPAND | wx.ALL)
        sub_sizer.Add(self.telephone_grid, 1, wx.EXPAND | wx.ALL)

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(sub_sizer, 0, wx.EXPAND)

        return this_sizer

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(self.create_sizer_heading(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(self.create_sizer_member_data(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(self.create_sizer_telephone(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(self.create_sizer_email(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(self.create_sizer_bottom_buttons(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_about(self, _event):
        """Create a message dialog box"""
        dlg = wx.MessageDialog(self,
            "About text.",
            "About Box Title", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished

    def on_cancel(self, _event):
        """Cancel"""
        self.Destroy()  # Close the frame

    def on_exit(self, _event):
        """Exit"""
        self.Close()  # Close the frame
