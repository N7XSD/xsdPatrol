"""
xsdPatrol common classes and functions
"""

# These classes are mostly sacks of attributes
#pylint: disable=too-few-public-methods
#pylint: disable=too-many-arguments
#pylint: disable=too-many-boolean-expressions
#pylint: disable=too-many-branches
#pylint: disable=too-many-instance-attributes

import datetime
import io
import logging
import os
import platform
import sys

import data
import settings

def calc_earned_hours(watch_num, shift_num, second_shift=False,
        student=False, instructor=False):
    """Returns earned hours for a shift
        This is very specific to Sun City Summerlin Security Patrol.
        Anyone else probably just wants to return the number of
        hours in a shift"""
    if student:
        return 4
    if watch_num == 0 and shift_num == 0:
        hours = 10
    elif watch_num == 0 and shift_num == 1:
        hours = 10
    elif watch_num == 0 and shift_num == 2:
        hours = 4
        if second_shift:
            hours += 2
    elif watch_num == 1 and shift_num == 0:
        hours = 4
        if second_shift:
            hours += 2
    elif watch_num == 1 and shift_num == 1:
        hours = 4
        if second_shift:
            hours += 2
    elif watch_num == 1 and shift_num == 2:
        hours = 7
        if second_shift:
            hours += 2
    else:
        # We should never get here but if we do,
        # give the user a funny looking number rather
        # than stopping the program
        logging.debug("""common.calc_earned_hours()
                unable to calculate hours correctly.
                Method returned 88 instead.""")
        return 88
    if instructor:
        hours += 4
    return hours


def get_console_name():
    """Return the console ID"""

    # The assumption here is that we have only one dispatcher
    # on a computer and can use the node name for a console ID
    fqd_name = platform.node()
    host_name = fqd_name.partition(".")[0]
    return host_name


def get_work_week_start_d(date_d):
    """Return a date object for the first day of the work week for date"""
    first_day = 6       # Work week starts on Sunday
    earlier_td = datetime.timedelta(
        days=((date_d.weekday() - first_day) % 7))
    start_day_d = date_d - earlier_td
    return start_day_d


def init_logging():
    """Initialize logging

       Logging is what the program does to keep track of it's own
       progress.  Not to be confused with the log the program is
       intended to manage.  Dot those i's and cross those t's."""

    logging.basicConfig(format='%(levelname)s:%(message)s',
            filename=settings.LOGGING_FILE, encoding="utf-8",
            filemode="w", level=settings.LOGGING_LEVEL)
    logging.info("%s  %s", settings.ID_NAME, settings.ID_VER)
    logging.info(datetime.datetime.now().isoformat(" ", "seconds"))
    if os.name == "posix":
        logging.info(os.uname())
    elif os.name == "nt":
        logging.info(sys.getwindowsversion())
    else:
        logging.info("Running on %s", os.name)


class DispatchDbReports():
    """Import form Dispatch DB and create reports"""

    def dispatch_db_hours(self, cmn, output, start_d, end_d):
        """Return a StringIO object conaining an HTML reports showing
           hours recoreded between dates in the dispatch DB"""

        end1_d = end_d - datetime.timedelta(days=1)
        time_dict = {}
        te_list, watch_id_start, watch_id_end \
            = cmn.dat.get_wc_date_range(start_d, end_d)
        cmn.add_time_entries(time_dict, te_list)

        te_list = cmn.dat.get_dispatch_by_watch(watch_id_start, watch_id_end)
        cmn.add_time_entries(time_dict, te_list)

        te_list = cmn.dat.get_car_by_watch(watch_id_start, watch_id_end)
        cmn.add_time_entries(time_dict, te_list)

        te_list = cmn.dat.get_ic_by_watch(watch_id_start, watch_id_end)
        cmn.add_time_entries(time_dict, te_list)
#       for i in sorted(time_dict):
#           print(f'{i} : {time_dict[i]}')

        user_ids = set()
        for i in time_dict.values():
            for j in i:
                user_ids.add(j.user_id)

        name_dict = cmn.dat.get_full_name(user_ids)
        disp_name_dict = {}
        for i in sorted(name_dict):
#           print(f'{i} : {name_dict[i]}')
            if i == name_dict[i]:
                disp_name_dict[i] = i
            else:
#               disp_name_dict[i] = f'{name_dict[i]} ({i})'
                disp_name_dict[f'{name_dict[i]} ({i})'] = i

        for i in user_ids:
            try:
                for j in time_dict[i]:
                    j.user_name = name_dict[i]
            except KeyError:
                for j in time_dict[i]:
                    j.user_name = ''

        output.write('<html>\n')
        output.write('<body COLOR="black" BGCOLOR="white">\n')
        output.write('<h1>Dispatch Log Hours Extract</h1>\n')
        output.write(f'<h2>From {start_d} to {end1_d}</h2>\n')
        output.write('<p>Notes about hours.</p>\n')
        output.write('<ul>\n')
        output.write('''<li>Hours are extracted from the dispatch log
            database.</li>\n''')
        output.write('''<li>Date is the nominal date of the shift.
            Actual arrival time is not recorded in the database.</li>\n''')
        output.write('''<li>When hours are recorded as "99" they are
            converted to zero and "(no hours earned) is appended to the
            activity.</li>\n''')
#       output.write('''<li></li>\n''')
        output.write('</ul>\n')

        user_keys = list(time_dict.keys())
        for i in sorted(disp_name_dict):
            s = i.replace('###', '<font COLOR="red">###</font>')
            output.write(f'<p>{s}</p>\n')
            total_rec = 0.0
            output.write('<table>\n')
            output.write('<tr><th>Hours</th>'
                + '<th>Date</th></tr>'
                + '<th>Watch</th></tr>'
                + '<th>Shift</th></tr>'
                + '<th>Activity</th></tr>\n')
            for j in sorted(time_dict[disp_name_dict[i]]):
                total_rec += j.hours_rec
                date_st = j.service_date.strftime(cmn.stns.get_format_date())
                watch_st = str(j.watch_number + 1)
                if j.shift_number < 0:
                    shift_st = ""
                else:
                    shift_st = str(j.shift_number + 1)
                output.write(f'<tr><td style="text-align:right">'
                    + f'{j.hours_rec}</td>'
                    + f'<td ALIGN="center">{date_st}</td>'
                    + f'<td ALIGN="center">{watch_st}</td>'
                    + f'<td ALIGN="center">{shift_st}</td>'
                    + f'<td>{j.unit_id}</td></tr>\n')
            output.write(f'<tr><td style="text-align:right">{total_rec}</td>'
                + f'<td>TOTAL</td></tr>\n')
            output.write('</table>\n')

        output.write('</body>\n')
        output.write('</html>')


class Event():
    item_id = None
    watch_id = None
    shift_number = None
    time_dt = None
    code = None
    source = None
    location = None
    description = None


class Responder():
    resp_id = None
    is_active = True
    sort_index = 0
    name = None


class Ticket():
    ticket_state = "open"
    open_dt = None
    address = None
    responders = []
    cones_used = 0
    initial_event = None
    folowup_events = []


class TimeEntry():
    user_name = ""
    user_id = ""
    unit_id = ""
    service_date = None
    watch_number = 0
    shift_number = 0
    second_shift = False
    student = False
    instructor = False
    hours_rec = 0.0
    hours_calc = 0.0

    def __str__(self):
        return (
            f"{self.user_name:12}"
            f" {self.user_id:12}"
            f" {self.service_date}"
            f" {self.watch_id}"
            f" {self.shift_number}"
            f" {self.hours_calc}")

    def __hash__(self):
        return hash(user_id, unit_id, service_date, watch_number,
            shift_number)

    def __eq__(self, other):
        return (self.service_date == other.service_date
            and self.watch_number == other.watch_number
            and self.shift_number == other.shift_number)

    def __lt__(self, other):
        return (self.service_date < other.service_date
            or (self.service_date == other.service_date
            and self.watch_number < other.watch_number)
            or (self.service_date == other.service_date
            and self.watch_number == other.watch_number)
            and self.shift_number < other.shift_number)

    def get_display_name(self):
        return f"{self.user_name} ({self.user_id})"


class Common():
    """
    A collection of objects to pass around to various user interfaces
    (windows, etc.)
    """
    UNK = 0

    JOB_IDS = ["Unknown",
        "Dispatcher", "Disp. Trainee",
        "Driver", "Driver Trainee",
        "IC Officer", "IC Trainee",
        "Observer",
        "Watch Commander", "WC Trainee"]
    JOB_IDS_SHORT = ["UNK", "DI", "DIT", "DR", "DRT", "IC", "ICT",
        "OBS", "WC", "WCT"]
    DI = 1
    DIT = 2
    DR = 3
    DRT = 4
    IC = 5
    ICT = 6
    OBSERVER = 7
    WC = 8
    WCT = 9

    PLACE_MOBILITY = ["Unknown", "Fixed", "Portable", "Mobile"]
    FIXED = 1       # Does not move (i.e. a house)
    PORTABLE = 2    # Can be moved but is usually used from
                    # a single location (i.e. a travel trailer)
    MOBILE = 3      # Spends most of its service time moving (i.e. a car)

    RATINGS_1_5 = ["1 - Very Poor", "2", "3", "4", "5 - Very Good"]

    def __init__(self):
        logging.debug("Init common.Common")
        self.app_start_time_dt = datetime.datetime.now()

#       FIXME: Mess with the date just for testing
#       self.app_start_time_dt = datetime.datetime(
#           year=2024, month=3, day=20)
#       self.app_start_time_dt -= datetime.timedelta(days=365)
#       print(self.app_start_time_dt)

        self.stns = settings.Settings()
        self.dat = data.Data(self)
        self.dat.open_dispatch_db()

        self.activity_code_list = []
        self.area_list = []
        self.subarea_list = []
        self.responder_list = []

    def add_time_entries(self, time_dict, te_list):
        """Add a time recored to a user.  A new user is created,
        if needed"""
        for i in te_list:
#           user_key = f"{i.user_name} ({i.user_id})"
            user_key = i.user_id
            if user_key in time_dict:
                time_dict[user_key].append(i)
            else:
                time_dict[user_key] = [i]

    def get_active_activity_code_list(self):
        """Returns a list of (code, description) tuples where active is
        true"""
        active_list = []
        for i in self.activity_code_list:
            if i[0]:
                active_list.append([i[1], i[2]])
        return active_list

    def get_activity_code_description(self, code):
        """Return the description for an activity code"""
        for i in self.activity_code_list:
            if code == i[1]:
                return str(i[2])
        return "Code " + str(code)

    def get_activity_code_list(self):
        """Returns a list of (active, code, description) tuples"""
        return self.activity_code_list

    def get_responder_list(self):
        """Returns a list of Responder objects"""
        return self.responder_list

    def get_last_work_week(self, date_d):
        """Returns datetime.date objects for first day of @date_d work
        week and the first day of the following week"""

        start_d = get_work_week_start_d(date_d)
        end_d = start_d + datetime.timedelta(weeks=1)
        return start_d, end_d

    def normalize_shift_date(self, rec_dt):
        """Return nominal shift date, etc. given the recorded datetime"""
        length_shift = (24 / len(self.stns.get_names_watch())) / len(
            self.stns.get_names_shift())
        # Arbitrarily, times in the last quarter of a shift are early
        # arrivals for the next shift.
        temp_dt = rec_dt + datetime.timedelta(hours=length_shift / 4)
        start_d = temp_dt.date()
        watch_number = 0
        shift_number = 0
        # FIXME: Calculate the watch and shift numbers
        return start_d, watch_number, shift_number

    def normalize_watch_date(self, rec_dt):
        """Return nominal watch date, etc. given the recorded datetime"""
        length_watch = 24 / len(self.stns.get_names_watch())
        # Arbitrarily, times in the last quarter of a watch are early
        # arrivals for the next watch.
        temp_dt = rec_dt + datetime.timedelta(hours=length_watch / 4)
        start_d = temp_dt.date()
        watch_number = 0
        # FIXME: Calculate the watch number
        return start_d, watch_number

    def set_activity_code_list(self, ac_list):
        """Sets a list of (active, code, description) tuples"""
        self.activity_code_list = ac_list

    def set_activity_code_item(self, index, is_active):
        self.activity_code_list[index][0] = is_active

    def set_responder_list(self, r_list):
        """Sets a list of (active, code, description) tuples"""
        self.responder_list = r_list
