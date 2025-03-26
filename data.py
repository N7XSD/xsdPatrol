"""
A place to keep data
"""

import datetime
import logging

def full_name(last_name, first_name, pref_name):
    """Return the full name as a string"""
    if not pref_name or pref_name == first_name:
        name = f"{first_name} {last_name}"
    else:
        name = f'{first_name} "{pref_name}" {last_name}'
    return name

class Data():
    """
    A class to manage data
    """
    # All functions and methods must return date time values as
    # datetime objects.  They must accept date time as datetime
    # objects and convert to the database native format.  For SQLite
    # we use ISO date strings.

    def __init__(self, cmn):
        logging.debug("Init data.Data")
        self.cmn = cmn
#       self.con = sqlite3.connect(cmn.stns.db_pathname)
        logging.info("    connected to sqlite3 db \'%s\'",
            cmn.stns.db_pathname)
#       self.cur = self.con.cursor()
