"""
wxPython (GUI) interface for xsdPatrol time keeping module
"""

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements

import datetime
import logging
import wx
#import wx.adv
#import wx.grid

import common
import commonwx


class TimeImportDispatchHours(commonwx.CommonFrame):
    """
    Window for importing hours from the dispatch DB
    """

    def __init__(self, parent, cmn):
        wx.Frame.__init__(self, parent,
            title="Import Dispatch DB Hours")
        logging.debug("Init timeimportdi.TimeImportDispatchHours")
        self.pnl = wx.Panel(self, name="pnl")
        self.cmn = cmn
        self.working_d = (self.cmn.app_start_time_dt
            - datetime.timedelta(weeks=1)).date()

        # Create the menubar
        menu_bar = self.create_menu_bar()
        self.SetMenuBar(menu_bar)

        # Layout sizers
        sizer_main = self.create_sizer_main()
        self.pnl.SetSizer(sizer_main)
        self.pnl.SetAutoLayout(1)
        sizer_main.Fit(self)

        self.cmn.get_last_work_week(self.working_d)

        self.Show()

    def create_sizer_spnl1(self):
        """Scroll panel 1 holds a list of things"""

        self.spnl1 = wx.ScrolledWindow(self.pnl, name="spnl1")
        self.spnl1.AlwaysShowScrollbars()
        sizer_spnl1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_spnl1.Add(self.spnl1)
        sizer_box1_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box1_main.Add(sizer_spnl1)

        (start_d, end_d) = self.cmn.get_last_work_week(self.working_d)

        te_list, watch_id_start, watch_id_end \
            = self.cmn.dat.get_wc_date_range(start_d, end_d)
        time_dict = {}
        self.cmn.add_time_entries(time_dict, te_list)

        te_list = self.cmn.dat.get_dispatch_by_watch(watch_id_start, watch_id_end)
        self.cmn.add_time_entries(time_dict, te_list)

        te_list = self.cmn.dat.get_car_by_watch(watch_id_start, watch_id_end)
        self.cmn.add_time_entries(time_dict, te_list)

        te_list = self.cmn.dat.get_ic_by_watch(watch_id_start, watch_id_end)
        self.cmn.add_time_entries(time_dict, te_list)

        self.name_dict = self.cmn.dat.get_full_name(time_dict.keys())

        # People and their hours
        hello_world = wx.StaticText(self.spnl1, label="Hello, World!")
        labels_people_names =[]
        sizers_people = []
        sizers_boxes = []
        for i in sorted(self.name_dict, key=self.name_dict.get):
#           sizers_people.append(wx.BoxSizer(wx.HORIZONTAL))
            b = wx.BoxSizer(wx.VERTICAL)
            sizers_boxes.append(b)

            t = wx.StaticText(self.spnl1, label=f"{self.name_dict[i]} ({i})")
            labels_people_names.append(t)
            b.Add(t)
            sizer_spnl1.Add(b)
        return sizer_spnl1

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""

        # Static text
        label_dl_extract = wx.StaticText(self.pnl,
            label="Dispatch Log Hours Extract")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        exit_button = wx.Button(self.pnl, wx.ID_EXIT)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_exit, exit_button)

        # BOX 0
        # Headings
        sizer_dl_extract = wx.BoxSizer(wx.HORIZONTAL)
        sizer_box0_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box0_main.Add(label_dl_extract)

        # BOX 1
        # A scrolled panel
        sizer_box1_main = self.create_sizer_spnl1()

        # BOX n
        # Create a sizer to hold the buttons
        sizer_box1_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box1_main.Add(wx.BoxSizer(wx.HORIZONTAL))

        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_button.AddStretchSpacer()
        sizer_button.Add(exit_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetContainingWindow(self.pnl)
        sizer_main.Add(sizer_box0_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_box1_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main
