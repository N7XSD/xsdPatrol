"""
wxPython (GUI) interface for xsdPatrol time keeping module
"""

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements

import logging
import wx

import common
import commonwx


class EditTicket(commonwx.CommonFrame):
    """
    Window used to edit a ticket
    """

    area_list = ["UNKNOWN"]
    subarea_list = ["UNK"]
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

        if self.cmn.area_list:
            self.area_list = self.cmn.area_list
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
            self.ticket = ticket
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

    def create_sizer_address(self):
        """The address sizer holds controls for the address"""
        # Static text
        address_label = wx.StaticText(self.pnl, label="Address")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        self.address_ctrl = wx.TextCtrl(self.pnl, value=self.ticket_address)
        area_ctrl = wx.Choice(self.pnl, choices=self.area_list)
        area_ctrl.SetSelection(0)

        subarea_ctrl = wx.Choice(self.pnl, choices=self.subarea_list)
        subarea_ctrl.SetSelection(0)

        sizer_addr_ctrl = wx.BoxSizer(wx.HORIZONTAL)
        sizer_addr_ctrl.Add(self.address_ctrl, 1)
        sizer_addr_ctrl.Add(area_ctrl, 0)
        sizer_addr_ctrl.Add(subarea_ctrl, 0)

        sizer_box = wx.BoxSizer(wx.VERTICAL)
        sizer_box.Add(address_label, 0)
        sizer_box.Add(sizer_addr_ctrl, 1, wx.EXPAND)

        return(sizer_box)

    def create_sizer_details(self):
        """The details sizer holds controls for the details"""
        # Static text
        details_label = wx.StaticText(self.pnl, label="Initial Event Details")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        initial_desc_ctrl = wx.TextCtrl(self.pnl,
            value=self.initial_details,
            style=(wx.TE_MULTILINE + wx.TE_READONLY))

        sizer_desc_ctrl = wx.BoxSizer(wx.HORIZONTAL)
        sizer_desc_ctrl.Add(initial_desc_ctrl, 1)

        sizer_box = wx.BoxSizer(wx.VERTICAL)
        sizer_box.Add(details_label, 0)
        sizer_box.Add(sizer_desc_ctrl, 1, wx.EXPAND)

        return sizer_box

    def create_sizer_followup(self):
        """The followup sizer holds controls for the followup list"""
        # Static text
        followup_label = wx.StaticText(self.pnl, label="Followup Events")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        self.followup_list = wx.ListCtrl(self.pnl, style=wx.LC_REPORT)

        self.build_followup_list(self.followup_list,
            self.ticket_folowup_events)

        sizer_followup_list = wx.BoxSizer(wx.HORIZONTAL)
        sizer_followup_list.Add(self.followup_list, 1, wx.EXPAND)

        sizer_box = wx.BoxSizer(wx.VERTICAL)
        sizer_box.Add(followup_label, 0)
        sizer_box.Add(sizer_followup_list, 1, wx.EXPAND)

        return sizer_box

    def create_sizer_footer(self):
        """The footer sizer holds controls for the footer"""
        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        add_followup_button = wx.Button(self.pnl, wx.ID_ANY,
            label="Add Followup Event")
        cancel_button = wx.Button(self.pnl, wx.ID_CANCEL)
        save_button = wx.Button(self.pnl, wx.ID_SAVE)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_add_event,
            add_followup_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_save, save_button)

        # Create a sizer to hold the buttons
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_button.Add(add_followup_button, 0)

        sizer_button.AddStretchSpacer()
        sizer_button.Add(cancel_button, 0)
        sizer_button.Add(save_button, 0)

        return sizer_button

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
        and any needed static text"""

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
        sizer_box0_main = self.create_sizer_header()
        sizer_box1_main = self.create_sizer_address()
        sizer_box2_main = self.create_sizer_responder()
        sizer_box3_main = self.create_sizer_details()
        sizer_box4_main = self.create_sizer_followup()
        sizer_box5_main = self.create_sizer_footer()

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
        sizer_main.Add(sizer_box5_main, 0, wx.EXPAND | wx.ALL,
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
        self.ticket.ticket_state = self.state_ctrl.GetSelection() + 1

        self.ticket.open_dt = self.ticket_open_dt
        self.ticket.address = self.address_ctrl.GetValue()
        self.ticket.cones_used = self.cones_ctrl.GetValue()
        self.ticket.initial_event = self.ticket_initial_event
        self.cmn.dat.save_ticket(self.ticket)
        self.Close()
