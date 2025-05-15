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
        commonwx.CommonFrame.__init__(self, parent, cmn,
            "Import Dispatch DB Hours")
        logging.debug("Init timeimportdi.TimeImportDispatchHours")
        working_d = (self.cmn.app_start_time_dt
            - datetime.timedelta(weeks=1)).date()
        self.cmn.get_last_work_week(working_d)

        self.Show()
