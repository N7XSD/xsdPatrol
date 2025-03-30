"""
wxPython (GUI) interface for xsdPatrol time keeping module
"""

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements

import datetime
import logging
#import wx.adv
#import wx.grid

#import activitywx
#import peoplewx
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

        # Header
        print("xsdPatrol Timekeeping")
        print("=====================")
        print()

        working_d = (self.cmn.app_start_time_dt
            - datetime.timedelta(weeks=1)).date()
        print("Working Date: %s" % working_d)

        (start_d, end_d) = self.cmn.get_last_work_week(working_d)
        print("Date Range: %s -- %s" % (start_d, end_d))

        te_list_wc = cmn.dat.get_wc_date_range(start_d, end_d)
        (watch_id_start, watch_id_end) = cmn.get_watch_range(te_list_wc)
        print("Watch Range: %s -- %s" % (watch_id_start, watch_id_end))

        print()
        if te_list_wc:
            for i in te_list_wc:
                print(i)
        else:
            print("I got nothin'")

        print()
        print(seperator_st)
        print()


if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    _ = TimekeepingMain(common_stuff)
