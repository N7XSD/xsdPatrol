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

    def __init__(self, parent, cmn, item):
        super().__init__(parent, cmn)
        self.pnl = wx.Panel(self)
        logging.debug("Init wx_member_edit.MemberEdit")

        self.cmn = cmn
        self.item = item
        self.member_id = -99
        self.user_name_logdb = ""
        self.surname = ""
        self.given_name = ""
        self.nickname = ""
        self.SetTitle("Basic Member Data")

        try:
            self.member_id = item.member_id
            self.user_name_logdb = item.user_name_logdb
            self.surname = item.surname
            self.given_name = item.given_name
            self.nickname = item.nickname
            self.SetTitle(f"Member ID: {self.member_id}")
        except Exception as e:
            print(e)
            # FIXME: Raise something,
            # without a data we can't get any farther


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

    def create_sizer_heading(self):
        """Create a sizer to hold some text at the top of our frame"""

        # Static text
        label_heading = wx.StaticText(self.pnl,
            label="Basic Member Data")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.

        # Bind widgets to methods

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(label_heading, 0)

        return this_sizer

    def create_sizer_member_data(self):
        """The main sizer holds member data and labels"""

        label_size = wx.Size(96, 16)
        line_gap = 8

        # Static text
        label_member_id = wx.StaticText(self.pnl, label="MemberID:  ",
            style=wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL,
            size=label_size)
        label_given_name = wx.StaticText(self.pnl, label="Given Name:  ",
            style=wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL,
            size=label_size)
        label_nickname = wx.StaticText(self.pnl, label="Nickname:  ",
            style=wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL,
            size=label_size)
        label_surname = wx.StaticText(self.pnl, label="Surname:  ",
            style=wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL,
            size=label_size)

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        member_id_ctrl = wx.TextCtrl(self.pnl, wx.ID_ANY,
            str(self.member_id), style=wx.TE_READONLY)
        given_name_ctrl = wx.TextCtrl(self.pnl, wx.ID_ANY,
            str(self.given_name))
        nickname_ctrl = wx.TextCtrl(self.pnl, wx.ID_ANY,
            str(self.nickname))
        surname_ctrl = wx.TextCtrl(self.pnl, wx.ID_ANY,
            str(self.surname))

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
        this_sizer.AddSpacer(line_gap)
        this_sizer.Add(sub_sizer_2, 0, wx.EXPAND | wx.ALL)
        this_sizer.AddSpacer(line_gap)
        this_sizer.Add(sub_sizer_3, 0, wx.EXPAND | wx.ALL)
        this_sizer.AddSpacer(line_gap)
        this_sizer.Add(sub_sizer_4, 0, wx.EXPAND | wx.ALL)
        return this_sizer

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(self.create_sizer_heading(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(self.create_sizer_member_data(),
            1, wx.EXPAND | wx.ALL,
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
