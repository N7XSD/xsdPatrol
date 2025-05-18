"""
wxPython (GUI) interface for xsdPatrol time keeping module
"""

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements

import datetime
import io
import logging
import wx

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

        self.Show()

    def create_menu_bar(self):
        """Create the menu bar"""

        # Create MenuItems
        # Note: About and Exit are moved to the application menu in macOS
        about_mitem = wx.MenuItem(None, wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.on_about, about_mitem)

        exit_mitem = wx.MenuItem(None, wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_mitem)

        import_di_mitem = wx.MenuItem(None, wx.ID_ANY,
            "Import Dispatch DB Hours")
        self.Bind(wx.EVT_MENU, self.on_import_di_db_hours, import_di_mitem)

        # File menu
        file_menu = wx.Menu()
        file_menu.Append(import_di_mitem)
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
        working_d = (self.cmn.app_start_time_dt
            - datetime.timedelta(weeks=1)).date()
        self.cmn.get_last_work_week(working_d)

        # Static text
        label_start_date = wx.StaticText(self.pnl, label="Test Date")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        ctrl_start_date = wx.TextCtrl(self.pnl,
            style=wx.TE_READONLY)
        exit_button = wx.Button(self.pnl, wx.ID_EXIT)

        ctrl_start_date.SetValue(working_d.isoformat())

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_exit, exit_button)

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

        sizer_button.AddStretchSpacer()
        sizer_button.Add(exit_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_box0_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_import_di_db_hours(self, _event):
        """Open Dispatch DB import window"""
#       timeimportdi.TimeImportDispatchHours(self, self.cmn)

        # Ask the user to choose start and end dates.
        # FIXME: Not really.  Pick some for testing.
        working_d = (self.cmn.app_start_time_dt
            - datetime.timedelta(weeks=1)).date()
        (start_d, end_d) = self.cmn.get_last_work_week(working_d)

        reports = common.DispatchDbReports()
        web_page = io.StringIO()
        reports.dispatch_db_hours(self.cmn, web_page, start_d, end_d)
        web_page.seek(0)
        report_viewer = commonwx.ShowHTML(self, self.cmn, web_page,
            "Import from Dispatch DB")
        report_viewer.Show()
        web_page.close()


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
