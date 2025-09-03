"""
wxPython (GUI) interface for xsdPatrol time keeping module
"""

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements

import logging
import wx

import common
import commonwx
import data


class ChangeFilter(commonwx.CommonFrame):
    """
    Window used to select a ticket
    """

    def __init__(self, parent, cmn, title):
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init ticketwx.ChangeFilter")
        self.cmn = cmn

        self.Show()

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

        codes = []
        self.selection_ctrl = []
        for j in self.cmn.get_activity_code_list():
            codes.append(j[1])
            if j[1] >= 1000 and j[1] <= 9999:
                desc = str(j[1]) + " " + j[2]
                desc = desc[:2] + "-" + desc[2:]
            else:
                desc = j[2]
            cb = wx.CheckBox(self.pnl, label=desc)
            cb.SetValue(j[0])
            self.selection_ctrl.append(cb)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_ok, ok_button)

        # BOX n - 1
        # Choices
        sizer_choice = wx.BoxSizer(wx.VERTICAL)
        for i in self.selection_ctrl:
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
        for i, j in enumerate(self.selection_ctrl):
            self.cmn.set_activity_code_item(i, j.IsChecked())
        self.Close()    # Close the frame


class SelectTicket(commonwx.CommonFrame):
    """
    Window used to select a ticket
    """

    def __init__(self, parent, cmn, title):
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init ticketwx.SelectTicket")

        self.Show()

    def build_selection_list(self, s_list, include_closed=False):
        """Data, pretty data"""
        self.ticket_list = self.cmn.dat.get_ticket_list(include_closed)
        s_list.AppendColumn("State", wx.LIST_FORMAT_LEFT, 64)
        s_list.AppendColumn("Time Opened", wx.LIST_FORMAT_LEFT, 128)
        s_list.AppendColumn("Description", wx.LIST_FORMAT_LEFT, 256)
        for i in self.ticket_list:

            # FIXME: We should look this up in the Ticket_State table
            state_st = str(i.ticket_state)
            if i.ticket_state == 1:
                state_st = ""
            elif i.ticket_state == 2:
                state_st = "Closed"

            index = s_list.InsertItem(s_list.GetItemCount(), state_st)
            s_list.SetItem(index, 1, str(i.open_dt))
            s_list.SetItem(index, 2, str(i.initial_event.description))

    def create_menu_bar(self):
        """No menu bar"""
        return None

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""
        # Static text

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        self.selection_list = wx.ListCtrl(self.pnl, style=wx.LC_REPORT)
        self.include_closed_ctrl = wx.CheckBox(self.pnl,
            label="Include closed")
        refresh_button = wx.Button(self.pnl, wx.ID_ANY, "Refresh")
        cancel_button = wx.Button(self.pnl, wx.ID_CANCEL)
        new_button = wx.Button(self.pnl, wx.ID_NEW)
        self.open_button = wx.Button(self.pnl, wx.ID_ANY, "Open")
        self.open_button.Enable(False)

        self.build_selection_list(self.selection_list)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select_item,
            self.selection_list)
        self.pnl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_open,
            self.selection_list)

        self.pnl.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_new, new_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_open, self.open_button)
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
        sizer_choice.Add(self.include_closed_ctrl, 0)

        # BOX n
        # Create a sizer to hold the buttons
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_button.Add(refresh_button, 0)

        sizer_button.AddStretchSpacer()
        sizer_button.Add(cancel_button, 0)
        sizer_button.Add(new_button, 0)
        sizer_button.Add(self.open_button, 0)

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
        SelectEvent(self, self.cmn, "Select Initial Event")

    def on_open(self, _event):
        """Open an existing ticket"""
        if isinstance(_event, wx._core.ListEvent):
            disp_item = self.ticket_list[_event.GetIndex()]
            EditTicket(self, common_stuff, "Edit Ticket", ticket=disp_item)
        elif isinstance(_event, wx._core.CommandEvent):
            disp_item = self.ticket_list[
                self.selection_list.GetFirstSelected()]
            EditTicket(self, common_stuff, "Edit Ticket", ticket=disp_item)
        else:
            logging.error("SelectTicket.on_open wasn't expecting an object"
                + " of type %s", type(_event))

    def on_refresh(self, _event):
        """Refresh the window"""
        self.selection_list.ClearAll()
        self.build_selection_list(self.selection_list,
            self.include_closed_ctrl.GetValue())

    def on_select_item(self, _event):
        """An item is selected"""
        self.open_button.Enable(True)


class SelectEvent(commonwx.CommonFrame):
    """
    Window used to select an event
    """

    def __init__(self, parent, cmn, title):
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init ticketwx.SelectEvent")

        self.parent = parent
        self.Show()

    def build_selection_list(self, s_list):
        """Data, pretty data"""

        act_code_list_1 = self.cmn.get_active_activity_code_list()
        act_code_list_2 = []
        for i in act_code_list_1:
            act_code_list_2.append(i[0])

        self.event_list = self.cmn.dat.get_event_list(act_code_list_2)
        item_list = []
        for j in self.event_list:
            if j.code >= 1000 and j.code <= 9999:
                desc = str(j.code) + " " + j.description
                desc = desc[:2] + "-" + desc[2:]
            else:
                desc = j.description
            item_list.append([str(j.time_dt), desc])
        s_list.AppendColumn("Time", wx.LIST_FORMAT_LEFT, 128)
        s_list.AppendColumn("Description", wx.LIST_FORMAT_LEFT, 256)
        index = None
        for i in item_list:
            index = s_list.InsertItem(s_list.GetItemCount(), i[0])
            for j, j_text in enumerate(i[1:]):
                s_list.SetItem(index, j+1, j_text)
        if isinstance(index, int):
            s_list.EnsureVisible(index)

    def create_menu_bar(self):
        """No menu bar"""
        return None

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""
        # Static text

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        self.selection_list = wx.ListCtrl(self.pnl,
            style=wx.LC_REPORT + wx.LC_SINGLE_SEL + wx.LC_HRULES)
        self.build_selection_list(self.selection_list)

        filter_button = wx.Button(self.pnl, wx.ID_ANY, "Filter")
        refresh_button = wx.Button(self.pnl, wx.ID_ANY, "Refresh")
        cancel_button = wx.Button(self.pnl, wx.ID_CANCEL)

        self.ok_button = wx.Button(self.pnl, wx.ID_OK)
        self.ok_button.Enable(False)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select_item,
            self.selection_list)
        self.pnl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_ok,
            self.selection_list)

        self.pnl.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_filter, filter_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_ok, self.ok_button)
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
        sizer_button.Add(self.ok_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_box0_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_filter(self, _event):
        """Change the data filter"""
        ChangeFilter(self, self.cmn, "Change Filter")

    def on_ok(self, _event):
        """Open a new ticket using selected event"""
        if isinstance(_event, wx._core.ListEvent):
            disp_event = self.event_list[_event.GetIndex()]
            EditTicket(self.parent, common_stuff, "Edit Ticket", event=disp_event)
        elif isinstance(_event, wx._core.CommandEvent):
            disp_event = self.event_list[
                self.selection_list.GetFirstSelected()]
            EditTicket(self.parent, common_stuff, "Edit Ticket", event=disp_event)
        else:
            logging.error("SelectTicket.on_ok wasn't expecting an object"
                + " of type %s", type(_event))
        self.Close()    # Close the SelectEvent frame

    def on_refresh(self, _event):
        """Refresh the window"""
#       self.ok_button.Enable(True)

    def on_select_item(self, _event):
        """An item is selected"""
        self.ok_button.Enable(True)


class EditTicket(commonwx.CommonFrame):
    """
    Window used to edit a ticket
    """

    ticket = None
    ticket_address = ""
    ticket_code_desc = "## MISSING CODE DESCRIPTION ##"
    ticket_cones_used = 0
    ticket_folowup_events = []
    ticket_initial_event = None
    ticket_new = None
    ticket_responders = []
    ticket_state = 1    # Open
    initial_details = "## MISSING DETAILS ##"

    def __init__(self, parent, cmn, title, ticket=None, event=None):
#       commonwx.CommonFrame.__init__(self, parent, cmn, title)
        wx.Frame.__init__(self, parent, title=title)
        logging.debug("Init ticketwx.EditTicket")

        self.SetMinSize(wx.Size(256, 256))
        self.pnl = wx.Panel(self)
        self.cmn = cmn

        self.area_list = ["UNKNOWN"]
        if self.cmn.area_list:
            self.area_list = self.cmn.area_list
        self.subarea_list = ["UNK"]
        if self.cmn.subarea_list:
            self.subarea_list = self.cmn.subarea_list

        if isinstance(event, common.Event):
            self.ticket_new = True
            self.ticket = common.Ticket()
            self.ticket_initial_event = event
            self.ticket_open_dt = str(event.time_dt)
            self.initial_details = event.description
        elif isinstance(ticket, common.Ticket):
            self.ticket_new = False
            self.ticket_address = str(ticket.address)
            self.ticket_cones_used = int(ticket.cones_used)
            self.ticket_folowup_events = ticket.folowup_events
            self.ticket_initial_event = ticket.initial_event
            self.initial_details = ticket.initial_event.description
            self.ticket_open_dt = ticket.open_dt
            self.ticket_responders = ticket.responders
            self.ticket_state = int(ticket.ticket_state)
        else:
            logging.error("Was expecting a Ticket or Event")
        self.ticket_code_desc = \
            self.cmn.get_activity_code_description(
                self.ticket_initial_event.code)

        # Layout sizers
        sizer_main = self.create_sizer_main()
        self.pnl.SetSizer(sizer_main)
        self.pnl.SetAutoLayout(1)
        sizer_main.Fit(self)
        self.Show()

    def build_followup_list(self, s_list, e_list):
        """Data, pretty data"""

        s_list.AppendColumn("Time", wx.LIST_FORMAT_LEFT, 128)
        s_list.AppendColumn("Description", wx.LIST_FORMAT_LEFT, 256)
        for i in e_list:
            if isinstance(i, common.Event):
                index = s_list.InsertItem(s_list.GetItemCount(),
                    str(i.time_dt))
                s_list.SetItem(index, 1, i.description)
            else:
                logging.error("Wasn't expecting an object"
                    + " of type %s", type(_event))
                break

    def create_menu_bar(self):
        """No menu bar"""
        return None

    def create_sizer_header(self):
        """This sizer holds labels and controls at the top of the frame."""

        state_name_list = []
        for i in self.cmn.state_list:
            state_name_list.append(i.name)

        # Static text
        cones_label = wx.StaticText(self.pnl, label="Cones Used")
        state_label = wx.StaticText(self.pnl, label="State")
        ticket_desc_label = wx.StaticText(self.pnl, label=self.ticket_code_desc)
        time_open_label = wx.StaticText(self.pnl, label="Open Time")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        self.state_ctrl = wx.Choice(self.pnl, choices=state_name_list)
        self.state_ctrl.SetSelection(self.ticket_state - 1)  # DB indexing one based

        self.cones_ctrl = wx.SpinCtrl(self.pnl, initial=self.ticket_cones_used)
        time_open_ctrl = wx.TextCtrl(self.pnl,
            value=str(self.ticket_open_dt), style=wx.TE_READONLY)

        sizer_cones = wx.BoxSizer(wx.VERTICAL)
        sizer_cones.Add(cones_label, 0)
        sizer_cones.Add(self.cones_ctrl, 0)

        sizer_open_time = wx.BoxSizer(wx.VERTICAL)
        sizer_open_time.Add(time_open_label, 0)
        sizer_open_time.Add(time_open_ctrl, 0)

        sizer_state = wx.BoxSizer(wx.VERTICAL)
        sizer_state.Add(state_label, 0)
        sizer_state.Add(self.state_ctrl, 0)

        sizer_details = wx.BoxSizer(wx.HORIZONTAL)
        sizer_details.Add(sizer_state, 0)
        sizer_details.AddSpacer(8)
        sizer_details.Add(sizer_cones, 0)
        sizer_details.AddStretchSpacer()
        sizer_details.Add(sizer_open_time, 0)

        sizer_box = wx.BoxSizer(wx.VERTICAL)
        sizer_box.Add(ticket_desc_label, 0)
        sizer_box.AddSpacer(8)
        sizer_box.Add(sizer_details, 0, wx.EXPAND)
        return sizer_box

    def create_sizer_responder(self):
        """The responder sizer holds controls for On Scene Responders
        and any neede static text"""

        if len(self.cmn.responder_list):
            # Static text
            responder_label = wx.StaticText(self.pnl, label="On Scene Responders")

            # Create text controls, check boxes, buttons, etc.
            # in tab traversal order.
            sizer_responder = wx.BoxSizer(wx.HORIZONTAL)
            responder_ctrl_list = []
            for resp in self.cmn.responder_list:
                ctrl = wx.CheckBox(self.pnl, label=resp.name)
                sizer_responder.Add(ctrl, 0)
                sizer_responder.AddSpacer(8)
                responder_ctrl_list.append(ctrl)

            sizer_box = wx.BoxSizer(wx.VERTICAL)
            sizer_box.Add(responder_label, 0)
            sizer_box.Add(sizer_responder)
            return(sizer_box)

        return None

    def create_sizer_main(self):
        """The main sizer holds everything the user will interact with"""
        # Static text
        address_label = wx.StaticText(self.pnl, label="Address")
        followup_label = wx.StaticText(self.pnl, label="Followup Events")
        details_label = wx.StaticText(self.pnl, label="Initial Event Details")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        self.address_ctrl = wx.TextCtrl(self.pnl, value=self.ticket_address)
        area_ctrl = wx.Choice(self.pnl, choices=self.area_list)
        area_ctrl.SetSelection(0)

        subarea_ctrl = wx.Choice(self.pnl, choices=self.subarea_list)
        subarea_ctrl.SetSelection(0)

        initial_desc_ctrl = wx.TextCtrl(self.pnl,
            value=self.initial_details,
            style=(wx.TE_MULTILINE + wx.TE_READONLY))
        self.followup_list = wx.ListCtrl(self.pnl, style=wx.LC_REPORT)
        add_followup_button = wx.Button(self.pnl, wx.ID_ANY,
            label="Add Followup Event")
        cancel_button = wx.Button(self.pnl, wx.ID_CANCEL)
        save_button = wx.Button(self.pnl, wx.ID_SAVE)

        self.build_followup_list(self.followup_list,
            self.ticket_folowup_events)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_add_event,
            add_followup_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_save, save_button)

        # BOX 0
        sizer_box0_main = self.create_sizer_header()

        # BOX 1
        sizer_addr_ctrl = wx.BoxSizer(wx.HORIZONTAL)
        sizer_addr_ctrl.Add(self.address_ctrl, 1)
        sizer_addr_ctrl.Add(area_ctrl, 0)
        sizer_addr_ctrl.Add(subarea_ctrl, 0)

        sizer_box1_main = wx.BoxSizer(wx.VERTICAL)
        sizer_box1_main.Add(address_label, 0)
        sizer_box1_main.Add(sizer_addr_ctrl, 1, wx.EXPAND)

        # BOX 2
        sizer_box2_main = self.create_sizer_responder()

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
#       sizer_choice.Add(self.include_closed_ctrl, 0)

        # BOX n
        # Create a sizer to hold the buttons
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_button.Add(add_followup_button, 0)

        sizer_button.AddStretchSpacer()
        sizer_button.Add(cancel_button, 0)
        sizer_button.Add(save_button, 0)

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_box0_main, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_box1_main, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        if isinstance(sizer_box2_main, wx.Sizer):
            sizer_main.Add(sizer_box2_main, 0, wx.EXPAND | wx.ALL,
                border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_box3_main, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_box4_main, 1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(sizer_button, 0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_add_event(self, _event):
        """Add a followup event to the Ticket"""

    def on_ticket_state(self, _event):
        """Toggle ticket between open and closed"""
        # FIXME: Instead of toggling between two states,
        # we should use a pull down to select the state
        if self.ticket_state == 2:  # Closed
            self.ticket_state = 1
            self.ticket_state_button.SetLabel("Close Ticket")
        else:
            self.ticket_state = 2
            self.ticket_state_button.SetLabel("Open Ticket")

    def on_save(self, _event):
        """Save ticket"""
        # DB indexing one based
        print(type(self.ticket))
        self.ticket.ticket_state = self.state_ctrl.GetSelection() + 1

        self.ticket.open_dt = self.ticket_open_dt
        self.ticket.address = self.address_ctrl.GetValue()
        self.ticket.cones_used = self.cones_ctrl.GetValue()
        self.ticket.initial_event = self.ticket_initial_event
        self.cmn.dat.save_ticket(self.ticket)
        self.Close()


if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    stns = common_stuff.stns
    data_stuff = common_stuff.dat
    common_stuff.set_activity_code_list(data_stuff.get_activity_codes())
    common_stuff.set_responder_list(data_stuff.get_responder_list())
    common_stuff.set_state_list(data_stuff.get_state_list())

    # Create the area and subarea lists.  In the future this will be
    # extracted from the addresses table (yet to be designed).
    common_stuff.area_list.append("Select Area")
    for i in range(4):
        common_stuff.area_list.append("Area " + str(i + 1))
    common_stuff.subarea_list.append("Select Unit")
    for i in range(50):
        common_stuff.subarea_list.append("Unit " + str(i + 1))

    app = wx.App(False)
    SelectTicket(None, common_stuff, "Select Ticket")
    app.MainLoop()
