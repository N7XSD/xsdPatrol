"""
wxPython (GUI) for accessing MemberDB
"""

import logging
import wx

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
