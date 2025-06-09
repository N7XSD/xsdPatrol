"""
wxPython (GUI) interface for xsdPatrol time keeping module
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
import timeimportdi


class TimekeepingMain(commonwx.CommonFrame):
    """
    Main window for time keeping module
    """

    def __init__(self, parent, cmn, title):
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init timekeepingwx.TimekeepingMain")
        self.reports = common.DispatchDbReports()
        self.html_print = wx.html.HtmlEasyPrinting(parentWindow=self)

        self.Show()

    def create_menu_bar(self):
        """Create the menu bar"""

        # Create MenuItems
        # Note: About and Exit are moved to the application menu in macOS
        about_mitem = wx.MenuItem(None, wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.on_about, about_mitem)

        exit_mitem = wx.MenuItem(None, wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_mitem)

        display_di_import_mitem = wx.MenuItem(None, wx.ID_PREVIEW,
            "Display Dispatch DB Hours")
        self.Bind(wx.EVT_MENU, self.on_display_import_di_db_hours,
            display_di_import_mitem)

        print_di_import_mitem = wx.MenuItem(None, wx.ID_ANY,
            "Print Dispatch DB Hours")
        self.Bind(wx.EVT_MENU, self.on_print_import_di_db_hours,
            print_di_import_mitem)

        # File menu
        file_menu = wx.Menu()
        file_menu.Append(display_di_import_mitem)
        file_menu.Append(print_di_import_mitem)
        file_menu.AppendSeparator()
        file_menu.Append(exit_mitem)

        # Help menu
        help_menu = wx.Menu()
        help_menu.Append(about_mitem)

        # Create the menubar
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")

        return menu_bar

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""
        self.working_d = (self.cmn.app_start_time_dt
            - datetime.timedelta(weeks=1)).date()
        self.start_d, self.end_d = self.cmn.get_last_work_week(self.working_d)

        # Static text
        label_start_date = wx.StaticText(self.pnl,
            label="Select any day in work week")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        ctrl_start_date = wx.adv.CalendarCtrl(self.pnl)
        print_button = wx.Button(self.pnl, wx.ID_PREVIEW)
        exit_button = wx.Button(self.pnl, wx.ID_EXIT)

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
        self.pnl.Bind(wx.EVT_BUTTON, self.on_exit, exit_button)
        self.Bind(wx.EVT_BUTTON, self.on_print_import_di_db_hours,
            print_button)

        self.pnl.Bind(wx.adv.EVT_CALENDAR,
            self.on_date_changed, ctrl_start_date)
        self.pnl.Bind(wx.adv.EVT_CALENDAR_PAGE_CHANGED,
            self.on_date_changed, ctrl_start_date)
        self.pnl.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED,
            self.on_date_changed, ctrl_start_date)

        # BOX 0
        # Headings
        sizer_heading_date = wx.BoxSizer(wx.HORIZONTAL)
        sizer_heading_date.Add(ctrl_start_date, 1)

        sizer_box0_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box0_main.Add(label_start_date)
        sizer_box0_main.Add(sizer_heading_date, 1, wx.EXPAND)

        # BOX n
        # Create a sizer to hold the buttons
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_button.Add(print_button, 0)

        sizer_button.AddStretchSpacer()
        sizer_button.Add(exit_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_box0_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_date_changed(self, _event):
        """Change the working date"""
        self.working_d = datetime.date.fromisoformat(
            _event.GetDate().FormatISODate())
#       print(self.working_d)
        self.start_d = common.get_work_week_start_d(self.working_d)
        self.end_d = self.start_d + datetime.timedelta(weeks=1)
#       print(self.start_d, self.end_d)

    def on_display_import_di_db_hours(self, _event):
        """Open a window to display data imported from dispatch DB"""
#       timeimportdi.TimeImportDispatchHours(self, self.cmn)

        web_page = io.StringIO()
        self.reports.dispatch_db_hours(self.cmn, web_page, self.start_d,
            self.end_d)
        web_page.seek(0)
        report_viewer = commonwx.ShowHTML(self, self.cmn, web_page,
            "Import from Dispatch DB")
        report_viewer.Show()
        web_page.close()

    def on_print_import_di_db_hours(self, _event):
        """Print data imported from dispatch DB"""

        web_page = io.StringIO()
        self.reports.dispatch_db_hours(self.cmn, web_page, self.start_d,
            self.end_d)
        web_page.seek(0)
        self.html_print.PreviewText(web_page.read())
#       web_page.seek(0)
#       self.html_print.PrintText(web_page.read())


if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    stns = common_stuff.stns
    app = wx.App(False)
    frame = TimekeepingMain(None, common_stuff,
        "Patrol Timekeeping Management")
#    frame.SetPosition(stns.get_window_pos_time())
#    frame.SetSize(stns.get_window_size_time())
    app.MainLoop()
