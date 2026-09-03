"""
wxPython (GUI) interface for importing time from dispatch db
"""

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements

import datetime
import io
import logging
import wx
import wx.adv
import wx.html

import common
import commonwx


class TimeImport(commonwx.CommonFrame):
    """
    Main window for importing time data
    """

    def __init__(self, parent, cmn):
        super().__init__(parent, cmn)
        self.pnl = wx.Panel(self)
        logging.debug("Init wx_time_import.TimeImport")

        self.cmn = cmn
        self.html_print = wx.html.HtmlEasyPrinting(parentWindow=self)
        self.SetTitle("Import Timekeeping Data From DispatchDB")

        # FIXME: These should come from the config file
        # 0o3554 x 0o070 (1900 x 1080)
        self.title_font = wx.Font(wx.FontInfo(0o20).Bold())
        self.data_font = wx.Font(
            wx.FontInfo().Family(wx.FONTFAMILY_TELETYPE))
        self.label_size = wx.Size(0o140, 0o20)
        self.line_gap = 0o10
        self.window_size = wx.Size(0o600, 0o600)

        # Create the menubar
        menu_bar = self.create_menu_bar()
        self.SetMenuBar(menu_bar)

        # Layout sizers
        sizer_main = self.create_sizer_main()
        self.pnl.SetSizer(sizer_main)
        self.pnl.SetAutoLayout(1)
        sizer_main.Fit(self)

#       self.SetMinSize(wx.Size(256, 256))
        self.SetSize(wx.Size(self.window_size))
        self.Show()

    def create_sizer_heading(self):
        """Create a sizer to hold some text at the top of our frame"""

        # Static text
        label_heading = wx.StaticText(self.pnl,
            label="Import Hours From Dispatch DB")
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

    def create_sizer_instructions(self):
        """The main sizer holds everthing the user will interact with"""

        # Static text
        label_start_date = wx.StaticText(self.pnl,
            label="Select any day in work week")

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(label_start_date)

        return this_sizer

    def create_sizer_select_date(self):
        """The main sizer holds everthing the user will interact with"""
        self.working_d = (self.cmn.app_start_time_dt
            - datetime.timedelta(weeks=1)).date()
        self.start_d, self.end_d = self.cmn.get_last_work_week(
            self.working_d)

        # Static text

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        ctrl_start_date = wx.adv.GenericCalendarCtrl(self.pnl)

        # wx.DateTime months start at zero
        working_wxd = wx.DateTime(self.working_d.day,
            self.working_d.month - 1, self.working_d.year)
        start_wxd = wx.DateTime(self.start_d.day,
            self.start_d.month - 1, self.start_d.year)
        end_wxd = wx.DateTime(self.end_d.day,
            self.end_d.month - 1, self.end_d.year)
        ctrl_start_date.SetDateRange(upperdate=end_wxd)
        ctrl_start_date.SetDate(start_wxd)

        # Bind widgets to methods
        self.pnl.Bind(wx.adv.EVT_CALENDAR,
            self.on_date_changed, ctrl_start_date)
        self.pnl.Bind(wx.adv.EVT_CALENDAR_PAGE_CHANGED,
            self.on_date_changed, ctrl_start_date)
        self.pnl.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED,
            self.on_date_changed, ctrl_start_date)

        # Use a vertical sizer to stack our window
        this_sizer = wx.BoxSizer(wx.HORIZONTAL)
        this_sizer.AddStretchSpacer()
        this_sizer.Add(ctrl_start_date, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        this_sizer.AddStretchSpacer()

        return this_sizer

    def create_sizer_bottom_buttons(self):
        """Create a sizer to hold the buttons"""

        # Static text

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        exit_button = wx.Button(self.pnl, wx.ID_EXIT)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_exit, exit_button)

        # Put it all together
        this_sizer = wx.BoxSizer(wx.HORIZONTAL)

        this_sizer.AddStretchSpacer()
        this_sizer.Add(exit_button, 0)

        return this_sizer

    def create_sizer_main(self):
        """The main sizer holds everything the user will interact with"""

        # Use a vertical sizer to stack our window
        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(self.create_sizer_heading(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        this_sizer.Add(self.create_sizer_select_date(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        this_sizer.Add(self.create_sizer_instructions(),
            1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        this_sizer.Add(self.create_sizer_bottom_buttons(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return this_sizer

    def on_date_changed(self, _event):
        """Change the working date"""
        self.working_d = datetime.date.fromisoformat(
            _event.Date.FormatISODate())
        logging.debug(f"Working date changed to: {self.working_d}")
        self.start_d = common.get_work_week_start_d(self.working_d)
        self.end_d = self.start_d + datetime.timedelta(weeks=1)
        logging.debug(f"start date: {self.start_d}, end date: {self.end_d}")

if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    stns = common_stuff.stns
    app = wx.App(False)
    frame = TimekeepingMain(None, common_stuff)
#   frame.SetPosition(stns.get_window_pos_time())
#   frame.SetSize(stns.get_window_size_time())
    app.MainLoop()
