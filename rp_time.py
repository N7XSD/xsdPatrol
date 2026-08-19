"""
Reports from dispatch log database
"""

import datetime
import logging

import db_dispatch

class DispatchDbReports():
    """Import form Dispatch DB and create reports"""

    def dispatch_db_hours(self, cmn, output, start_d, end_d):
        """Return a StringIO object conaining an HTML reports showing
           hours recoreded between dates in the dispatch DB"""

        self.cmn = cmn
        self.ddb = db_dispatch.DispatchDB(self.cmn)

        end1_d = end_d - datetime.timedelta(days=1)
        time_dict = {}
        te_list, watch_id_start, watch_id_end \
            = self.ddb.get_wc_date_range(start_d, end_d)
        cmn.add_time_entries(time_dict, te_list)

        te_list = self.ddb.get_dispatch_by_watch(watch_id_start,
            watch_id_end)
        cmn.add_time_entries(time_dict, te_list)

        te_list = self.ddb.get_car_by_watch(watch_id_start, watch_id_end)
        cmn.add_time_entries(time_dict, te_list)

        te_list = self.ddb.get_ic_by_watch(watch_id_start, watch_id_end)
        cmn.add_time_entries(time_dict, te_list)
##      for i in sorted(time_dict):
##          print(f'{i} : {time_dict[i]}')

        user_ids = set()
        for i in time_dict.values():
            for j in i:
                user_ids.add(j.user_id)

        name_dict = self.ddb.get_full_name(user_ids)
        disp_name_dict = {}
        for i in sorted(name_dict):
##          print(f'{i} : {name_dict[i]}')
            if i == name_dict[i]:
                disp_name_dict[i] = i
            else:
##              disp_name_dict[i] = f'{name_dict[i]} ({i})'
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
##      output.write('''<li></li>\n''')
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
            output.write(f'<tr><td style="text-align:right">'
                + f'{total_rec}</td><td>TOTAL</td></tr>\n')
            output.write('</table>\n')

        output.write('</body>\n')
        output.write('</html>')


