"""
wxPython (GUI) interface for xsdPatrol time keeping module
"""

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements

import logging
import wx

import common
import commonwx


class ChangeFilter(commonwx.CommonFrame):
    """
    Window used to select a ticket
    """

    def __init__(self, parent, cmn, title):
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init ticketwx.SelectTicket")

        self.Show()

    def build_selection_list(self):
        """Data, pretty data"""

        # Begin test data creation
        list_of_stuff = [
            (True, 1002, "Return to base"),
            (True, 1003, "Lunch / coffee Break"),
            (True, 1004, "Message received"),
            (True, 1005, "Radio check"),
            (True, 1006, "Receiving clearly"),
            (True, 1007, "Out of service"),
            (True, 1008, "In service"),
            (False, 1009, "Open Garage Door (Don't use)"),
            (True, 1111, "Open Garage Door"),
            (True, 1112, "911 Light"),
            (True, 1113, "House check"),
            (True, 1114, "Association property checked"),
            (True, 1115, "Accident"),
            (True, 1116, "Water problem"),
            (False, 1117, "Home Inv/Rob/Burg (Don't use)"),
            (True, 1118, "Suspicious situation"),
            (True, 1119, "Concern for resident"),
            (True, 1120, "Suspected SCAM"),
            (True, 1121, "Misc / Other"),
            (True, 1122, "Home invasion"),
            (True, 1123, "Robbery"),
            (True, 1124, "Burglary")]
        # End test data creation
        return list_of_stuff

    def create_menu_bar(self):
        """No menu bar"""
        return None

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""
        # Static text

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        cancel_button = wx.Button(self.pnl, wx.ID_CANCEL)
        ok_button = wx.Button(self.pnl, wx.ID_OK)

        choice_button = []
        for i in self.build_selection_list():
            if i[1] >= 1000 and i[1] <= 9999:
                desc = str(i[1]) + " " + i[2]
                desc = desc[:2] + "-" + desc[2:]
            else:
                desc = i[2]
            cb = wx.CheckBox(self.pnl, label=desc)
            cb.SetValue(i[0])
            choice_button.append(cb)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_ok, ok_button)

        # BOX n - 1
        # Choices
        sizer_choice = wx.BoxSizer(wx.VERTICAL)
        for i in choice_button:
            sizer_choice.Add(i, 0)

        # BOX n
        # Create a sizer to hold the buttons
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)

        sizer_button.AddStretchSpacer()
        sizer_button.Add(cancel_button, 0)
        sizer_button.Add(ok_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_choice, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_ok(self, _event):
        """Accept filter"""


class SelectTicket(commonwx.CommonFrame):
    """
    Window used to select a ticket
    """

    def __init__(self, parent, cmn, title):
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init ticketwx.SelectTicket")

        self.Show()

    def build_selection_list(self, s_list):
        """Data, pretty data"""

        # Begin test data creation
        list_of_stuff = [
            ("Closed", "2025-04-01 08:00", "one"),
            ("Closed", "2025-04-01 09:00", "two"),
            ("Closed", "2025-04-01 10:00", "three"),
            ("", "2025-04-01 11:00", "four"),
            ("", "2025-04-01 12:00", "five"),
            ("", "2025-04-01 13:00", "six"),
            ("", "2025-04-01 14:00", "seven"),
            ("", "2025-04-01 15:00", "eight"),
            ("", "2025-04-01 16:00", "nine"),
            ("", "2025-04-01 17:00", "last")]
        s_list.AppendColumn("State", wx.LIST_FORMAT_LEFT, 64)
        s_list.AppendColumn("Time Opened", wx.LIST_FORMAT_LEFT, 128)
        s_list.AppendColumn("Description", wx.LIST_FORMAT_LEFT, 256)
        for i in list_of_stuff:
            index = s_list.InsertItem(s_list.GetItemCount(), i[0])
            for j, j_text in enumerate(i[1:]):
                s_list.SetItem(index, j+1, j_text)
        # End test data creation

    def create_menu_bar(self):
        """No menu bar"""
        return None

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""
        # Static text

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        self.selection_list = wx.ListCtrl(self.pnl, style=wx.LC_REPORT)
        include_closed_ctrl = wx.CheckBox(self.pnl,
            label="Include closed")
        refresh_button = wx.Button(self.pnl, wx.ID_ANY, "Refresh")
        cancel_button = wx.Button(self.pnl, wx.ID_CANCEL)
        new_button = wx.Button(self.pnl, wx.ID_NEW)
        open_button = wx.Button(self.pnl, wx.ID_ANY, "Open")

        self.build_selection_list(self.selection_list)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_new, new_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_open, open_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_refresh, refresh_button)

        # BOX 0
        # Selection List
        sizer_selection_list = wx.BoxSizer(wx.HORIZONTAL)
        sizer_selection_list.Add(self.selection_list, 1, wx.EXPAND)

        sizer_box0_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box0_main.Add(sizer_selection_list, 1, wx.EXPAND)

        # BOX n - 1
        # Choices
        sizer_choice = wx.BoxSizer(wx.HORIZONTAL)
        sizer_choice.Add(include_closed_ctrl, 0)

        # BOX n
        # Create a sizer to hold the buttons
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_button.Add(refresh_button, 0)

        sizer_button.AddStretchSpacer()
        sizer_button.Add(cancel_button, 0)
        sizer_button.Add(new_button, 0)
        sizer_button.Add(open_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_box0_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_choice, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_new(self, _event):
        """Create a new ticket"""

    def on_open(self, _event):
        """Open an existing ticket"""

    def on_refresh(self, _event):
        """Refresh the window"""


class SelectEvent(commonwx.CommonFrame):
    """
    Window used to select an event
    """

    def __init__(self, parent, cmn, title):
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init ticketwx.SelectEvent")

        self.Show()

    def build_selection_list(self, s_list):
        """Data, pretty data"""

        # Begin test data creation
        list_of_stuff = [
            ("2025-04-01 08:00", "one"),
            ("2025-04-01 09:00", "two"),
            ("2025-04-01 10:00", "three"),
            ("2025-04-01 11:00", "four"),
            ("2025-04-01 12:00", "five"),
            ("2025-04-01 13:00", "six"),
            ("2025-04-01 14:00", "seven"),
            ("2025-04-01 15:00", "eight"),
            ("2025-04-01 16:00", "nine"),
            ("2025-04-01 17:00", "last")]
        s_list.AppendColumn("Time", wx.LIST_FORMAT_LEFT, 128)
        s_list.AppendColumn("Description", wx.LIST_FORMAT_LEFT, 256)
        for i in list_of_stuff:
            index = s_list.InsertItem(s_list.GetItemCount(), i[0])
            for j, j_text in enumerate(i[1:]):
                s_list.SetItem(index, j+1, j_text)
        # End test data creation

    def create_menu_bar(self):
        """No menu bar"""
        return None

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""
        # Static text

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        self.selection_list = wx.ListCtrl(self.pnl, style=wx.LC_REPORT)
        self.build_selection_list(self.selection_list)
        filter_button = wx.Button(self.pnl, wx.ID_ANY, "Filter")
        refresh_button = wx.Button(self.pnl, wx.ID_ANY, "Refresh")
        cancel_button = wx.Button(self.pnl, wx.ID_CANCEL)
        ok_button = wx.Button(self.pnl, wx.ID_OK)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_filter, filter_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_ok, ok_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_refresh, refresh_button)

        # BOX 0
        # Selection List
        sizer_selection_list = wx.BoxSizer(wx.HORIZONTAL)
        sizer_selection_list.Add(self.selection_list, 1, wx.EXPAND)

        sizer_box0_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box0_main.Add(sizer_selection_list, 1, wx.EXPAND)

        # BOX n
        # Create a sizer to hold the buttons
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_button.Add(filter_button, 0)
        sizer_button.Add(refresh_button, 0)

        sizer_button.AddStretchSpacer()
        sizer_button.Add(cancel_button, 0)
        sizer_button.Add(ok_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_box0_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_filter(self, _event):
        """Change the data filter"""

    def on_ok(self, _event):
        """The input is OK"""

    def on_refresh(self, _event):
        """Refresh the window"""


class EditTicket(commonwx.CommonFrame):
    """
    Window used to edit a ticket
    """

    def __init__(self, parent, cmn, title):
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init ticketwx.EditTicket")

        self.Show()

    # Made up for testing
    area_list = (
        "Area 1",
        "Area 2",
        "Area 3",
        "Area 4")
    subarea_list = (
        "Unit A",
        "Unit B",
        "Unit C",
        "Unit D")
    ticket_open_st = "2025-04-01 07:00"
    ticket_code_id = 1116
    ticket_code_desc = "Water problem"
    initial_details = """Irrigation leak at 3008 Crib Point Drive.  No answer at door.  DI called 702-896-0507 and left voice mail.  DR flagged leak location"""

    def build_followup_list(self, s_list):
        """Data, pretty data"""

        # Begin test data creation
        list_of_stuff = [
            ("2025-04-01 08:00", "one"),
            ("2025-04-01 09:00", "two"),
            ("2025-04-01 10:00", "three"),
            ("2025-04-01 11:00", "four"),
            ("2025-04-01 12:00", "five"),
            ("2025-04-01 13:00", "six"),
            ("2025-04-01 14:00", "seven"),
            ("2025-04-01 15:00", "eight"),
            ("2025-04-01 16:00", "nine"),
            ("2025-04-01 17:00", "last")]
        s_list.AppendColumn("Time", wx.LIST_FORMAT_LEFT, 128)
        s_list.AppendColumn("Description", wx.LIST_FORMAT_LEFT, 256)
        for i in list_of_stuff:
            index = s_list.InsertItem(s_list.GetItemCount(), i[0])
            for j, j_text in enumerate(i[1:]):
                s_list.SetItem(index, j+1, j_text)
        # End test data creation

    def create_menu_bar(self):
        """No menu bar"""
        return None

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""
        # Static text
        address_label = wx.StaticText(self.pnl, label="Address")
        cones_label = wx.StaticText(self.pnl, label="Cones Used  ")
        followup_label = wx.StaticText(self.pnl, label="Followup Events")
        details_label = wx.StaticText(self.pnl, label="Initial Event Details")
        responder_label = wx.StaticText(self.pnl, label="On Scene Responders")
        ticket_desc_label = wx.StaticText(self.pnl, label=self.ticket_code_desc)
        time_open_label = wx.StaticText(self.pnl, label="Open Time  ")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        address_ctrl = wx.TextCtrl(self.pnl)
        area_ctrl = wx.Choice(self.pnl, choices=self.area_list)
        subarea_ctrl = wx.Choice(self.pnl, choices=self.subarea_list)
        time_open_ctrl = wx.TextCtrl(self.pnl, value=self.ticket_open_st,
            style=wx.TE_READONLY)
        resp_wc_ctrl = wx.CheckBox(self.pnl, label="Watch Commander")
        resp_dr_ctrl = wx.CheckBox(self.pnl, label="Driver")
        resp_le_ctrl = wx.CheckBox(self.pnl, label="Law Enforcement")
        resp_fr_ctrl = wx.CheckBox(self.pnl, label="Fire and Rescue")
        resp_ambulance_ctrl = wx.CheckBox(self.pnl, label="Ambulance")
        resp_other_ctrl = wx.CheckBox(self.pnl, label="Other")
        cones_ctrl = wx.SpinCtrl(self.pnl)
        initial_desc_ctrl = wx.TextCtrl(self.pnl,
            value=self.initial_details,
            style=(wx.TE_MULTILINE + wx.TE_READONLY))
        self.followup_list = wx.ListCtrl(self.pnl, style=wx.LC_REPORT)
        close_button = wx.Button(self.pnl, wx.ID_ANY, label="Close Ticket")
        cancel_button = wx.Button(self.pnl, wx.ID_CANCEL)
        save_button = wx.Button(self.pnl, wx.ID_SAVE)

        self.build_followup_list(self.followup_list)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_close, close_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_save, save_button)

        # BOX 0
        sizer_box0_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_box0_main.Add(ticket_desc_label, 0)

        sizer_box0_main.AddStretchSpacer()
        sizer_box0_main.Add(time_open_label, 0)
        sizer_box0_main.Add(time_open_ctrl, 0)

        # BOX 1
        sizer_addr_ctrl = wx.BoxSizer(wx.HORIZONTAL)
        sizer_addr_ctrl.Add(address_ctrl, 1)
        sizer_addr_ctrl.Add(area_ctrl, 0)
        sizer_addr_ctrl.Add(subarea_ctrl, 0)

        sizer_box1_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box1_main.Add(address_label, 0)
        sizer_box1_main.Add(sizer_addr_ctrl, 1, wx.EXPAND)

        # BOX C
        sizer_boxC_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_boxC_main.Add(cones_label, 0)
        sizer_boxC_main.Add(cones_ctrl, 0)

        # BOX 2
        sizer_responder = wx.BoxSizer(wx.HORIZONTAL)
        sizer_responder.Add(resp_wc_ctrl)
        sizer_responder.Add(resp_dr_ctrl)
        sizer_responder.Add(resp_le_ctrl)
        sizer_responder.Add(resp_fr_ctrl)
        sizer_responder.Add(resp_ambulance_ctrl)
        sizer_responder.Add(resp_other_ctrl)

        sizer_box2_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box2_main.Add(responder_label, 0)
        sizer_box2_main.Add(sizer_responder)

        # BOX 3
        sizer_desc_ctrl = wx.BoxSizer(wx.HORIZONTAL)
        sizer_desc_ctrl.Add(initial_desc_ctrl, 1)

        sizer_box3_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box3_main.Add(details_label, 0)
        sizer_box3_main.Add(sizer_desc_ctrl, 1, wx.EXPAND)

        # BOX 4
        # Followup List
        sizer_followup_list = wx.BoxSizer(wx.HORIZONTAL)
        sizer_followup_list.Add(self.followup_list, 1, wx.EXPAND)

        sizer_box4_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box4_main.Add(followup_label, 0)
        sizer_box4_main.Add(sizer_followup_list, 1, wx.EXPAND)

        # BOX n - 1
        # Choices
#       sizer_choice = wx.BoxSizer(wx.HORIZONTAL)
#       sizer_choice.Add(include_closed_ctrl, 0)

        # BOX n
        # Create a sizer to hold the buttons
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_button.Add(close_button, 0)

        sizer_button.AddStretchSpacer()
        sizer_button.Add(cancel_button, 0)
        sizer_button.Add(save_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_box0_main, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_box1_main, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_box2_main, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_boxC_main, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_box3_main, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_box4_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_close(self, _event):
        """Cancel the window"""

    def on_save(self, _event):
        """Save ticket"""


if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    stns = common_stuff.stns
    app = wx.App(False)
    frame1 = SelectTicket(None, common_stuff, "Select Ticket")
    frame2 = SelectEvent(None, common_stuff, "Select Event")
    frame3 = ChangeFilter(None, common_stuff, "Change Filter")
    frame4 = EditTicket(None, common_stuff, "Edit Ticket")
    app.MainLoop()
