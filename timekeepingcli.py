"""
wxPython (GUI) interface for xsdPatrol time keeping module
"""

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements

import datetime
import logging

import common
#import data
#import settings


class TimekeepingMain():
    """
    Simple CLI for Timekeeping module
    """

    def __init__(self, cmn):
        logging.debug("Init timekeepingcli.TimekeepingMain")
        self.cmn = cmn
        seperator_st = 80 * '-'
        time_dict = {}

        # Header
        print("xsdPatrol Timekeeping")
        print("=====================")
        print()

        working_d = (self.cmn.app_start_time_dt
            - datetime.timedelta(weeks=1)).date()
        print("Working Date: %s" % working_d)

        (start_d, end_d) = self.cmn.get_last_work_week(working_d)
        print("Date Range: %s -- %s" % (start_d, end_d))

        te_list = cmn.dat.get_wc_date_range(start_d, end_d)
        (watch_id_start, watch_id_end) = cmn.get_watch_range(te_list)
        print("Watch Range: %s -- %s" % (watch_id_start, watch_id_end))
        cmn.add_time_entries(time_dict, te_list)

        te_list = cmn.dat.get_dispatch_by_watch(watch_id_start, watch_id_end)
        cmn.add_time_entries(time_dict, te_list)

        te_list = cmn.dat.get_car_by_watch(watch_id_start, watch_id_end)
        cmn.add_time_entries(time_dict, te_list)

        te_list = cmn.dat.get_ic_by_watch(watch_id_start, watch_id_end)
        cmn.add_time_entries(time_dict, te_list)

        print()
        print(seperator_st)

        name_dict = cmn.dat.get_full_name(time_dict.keys())
        for i in sorted(name_dict, key=name_dict.get):
            print()
            print(name_dict[i] + " (" + i + ")")
            total_rec = 0.0
            total_calc = 0.0
            for j in sorted(time_dict[i]):
                total_rec += j.hours_rec
                total_calc += j.hours_calc
                if j.hours_rec == j.hours_calc:
                    print(f"\t{j.service_date}"
                        f"\t{j.hours_rec:7} {j.hours_calc:8}\t{j.unit_id}")
                else:
                    print(f"*\t{j.service_date}"
                        f"\t{j.hours_rec:7} {j.hours_calc:8}\t{j.unit_id}")
            print("\t\t\t\t=======  =======")
            print(f"\t\t\t\t{total_rec:7} {total_calc:8}")


if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    _ = TimekeepingMain(common_stuff)
