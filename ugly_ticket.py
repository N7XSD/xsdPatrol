#   def get_event_list(self, code_list=None, start_date=None,
#           event_id_list=None):
#       """Return a list of events"""
#       start_date = datetime.datetime.now() - datetime.timedelta(days=5)
#       event_list = []
#       rows = None
#       if code_list is not None:
#           placeholders = ", ".join(["?"] * len(code_list))
#           sql_statement = """
#               SELECT Item_ID, Watch_ID, Shift_Number, Activity_DateTime,
#                   Ten_Code, Activity_Source, Location, Description
#               FROM Activities
#               WHERE IsActive AND Activity_DateTime > ?
#                   AND Ten_Code IN (""" + placeholders + ")"
##          print(sql_statement)
##          print(start_date, list(code_list))
##          print()
#           self.curs.execute(sql_statement, [start_date] + code_list)
#           rows = self.curs.fetchall()
#       elif event_id_list is not None:
#           placeholders = ", ".join(["?"] * len(event_id_list))
#           sql_statement = """
#               SELECT Item_ID, Watch_ID, Shift_Number, Activity_DateTime,
#                   Ten_Code, Activity_Source, Location, Description
#               FROM Activities
#               WHERE IsActive
#                   AND Item_ID IN (""" + placeholders + ")"
##          print(sql_statement)
##          print(event_id_list)
##          print()
#           self.curs.execute(sql_statement, event_id_list)
#           rows = self.curs.fetchall()
#       if rows is not None:
#           for i in rows:
#               event = common.Event()
#               event.item_id = i.Item_ID
#               event.watch_id = i.Watch_ID
#               event.shift_number = i.Shift_Number
#               event.time_dt = i.Activity_DateTime
#               event.code = i.Ten_Code
#               event.source = "unknown"
#               if i.Activity_Source == 1:
#                   event.source = "DISPATCH"
#               elif i.Activity_Source == 2:
#                   event.source = "WATCHDMDR"
#               event.location = i.Location
#               event.description = i.Description
#               event_list.append(event)
#       return event_list

#   def get_ticket_list(self, include_closed=False):
#       """Return list of Tickets"""
#       sql_statement = """
#           SELECT ID, ID_Event, State, Open, Address, Cones_Used
#           FROM Ticket"""
#       if not include_closed:
#           sql_statement += """ WHERE State <> 2"""
##      print(sql_statement)
##      print()
#       self.curs_patrol.execute(sql_statement)
#       rows = self.curs_patrol.fetchall()
#       ticket_list = []
#       if rows is not None:
#           for i in rows:
#               ticket = common.Ticket()
#               ticket.ticket_id = i.ID
#               ticket.ticket_state = i.State
#               ticket.open_dt = i.Open
#               ticket.address = i.Address
#               ticket.cones_used = i.Cones_Used
#               ticket.initial_event = i.ID_Event
#               ticket_list.append(ticket)

#       # ID_Event is the key to the event.  Replace those keys with
#       # Event objects.
#       event_numbers = set()
#       for i in ticket_list:


#           event_numbers.add(i.initial_event)
#       event_list = self.get_event_list(event_id_list=sorted(event_numbers))
#       event_dict = {}
#       for i in event_list:
#           event_dict[i.item_id] = i
#       for i in ticket_list:
#           i.initial_event = event_dict[i.initial_event]
#       return(sorted(ticket_list, key=lambda x: x.open_dt))

#   def get_responder_list(self):
#       """Returns a responder list."""

#       sql_statement = """
#           SELECT ID, Is_Active, Sort_Index, Responder_Name
#           FROM Responder
#           WHERE Is_Active
#           ORDER BY Sort_Index"""
##      print(sql_statement)
##      print()
#       self.curs_patrol.execute(sql_statement)
#       item_list = []
#       rows = self.curs_patrol.fetchall()
#       for i in rows:
#           item = common.Responder()
#           item.item_id = i.ID
#           item.sort_index = i.Sort_Index
#           item.name = str(i.Responder_Name)
#           item_list.append(item)
#       return(item_list)

#   def get_state_list(self):
#       """Ugly stub that returns a state list."""

#       # FIXME: this should come from a DB table
#       ugly_list = [
#           "Open",
#           "Closed"]
#       item_list = []
#       for i, name in enumerate(ugly_list):
#           item = common.TicketState()
#           item.item_id = i
#           item.name = str(name)
#           item_list.append(item)
#       return(item_list)

#   def save_ticket(self, ticket):
#       """This is where we put the ticket back in the DB.  This could
#       be a new or existing record."""

#       if ticket.ticket_id is None:
#            sql_statement = """
#                INSERT INTO Ticket
#                    (ID_Event, State, Open, Address, Cones_Used)
#                VALUES (?, ?, ?, ?, ?)"""
##           print(sql_statement)
##           print(ticket.initial_event.item_id, ticket.ticket_state,
##               ticket.open_dt, ticket.address, ticket.cones_used)
##           print()
#            self.curs_patrol.execute(sql_statement,
#               (ticket.initial_event.item_id, ticket.ticket_state,
#                ticket.open_dt, ticket.address, ticket.cones_used))
#            self.conn_patrol.commit()
#       else:
#            sql_statement = """
#                UPDATE Ticket
#                SET State = ?, Open = ?, Address = ?, Cones_Used = ?
#                WHERE ID = ?"""
##           print(sql_statement)
##           print(ticket.ticket_state, ticket.open_dt, ticket.address,
##               ticket.cones_used, ticket.ticket_id)
##           print()
#            self.curs_patrol.execute(sql_statement,
#               (ticket.ticket_state, ticket.open_dt, ticket.address,
#                ticket.cones_used, ticket.ticket_id))
#            self.conn_patrol.commit()
